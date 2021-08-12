import MeCab
import os
import argparse
import csv
import numpy as np
import pdb
import kanjize
import mojimoji
import re
from tqdm import tqdm
import jaconv
import pandas as pd
from regist_verbs import verb_types

current_idx = 0
fixed_list = []
word_type_stdout = 'which hinshi?\n1:名詞, 2:人名 3:地名, 4:動詞'
word_type_list = [
    [['名詞','固有名詞','一般','*','*','*'],4786],
    [['名詞','固有名詞','人名','*','*','*'],4788],
    [['名詞','固有名詞','地名','*','*','*'],4792],
    ['動詞',0]
]
matrix = pd.read_csv('./matrix.csv', names=['prev','target','cost'])

def calc_cost(cid_prev, cid_old, cid_new, c_extract):
    artic_cost_prev = calc_articulation_cost(cid_old, cid_prev)
    artic_cost = calc_articulation_cost(cid_new, cid_prev)
    cost_fixed = artic_cost_prev + int(c_extract) - (artic_cost + 1)

    return cost_fixed

def calc_articulation_cost(c_id, c_id_prev):
    c_id = int(c_id)
    c_id_prev = int(c_id_prev)
    return matrix[
        (matrix['prev'] == c_id_prev)
        & (matrix['target'] == c_id)]['cost'].values[0]

def select_word_types(idx):
    idx = int(idx) - 1
    if idx > len(word_type_list):
        print('this number cant\'t using')
        select_word_types(input_to_han(word_type_stdout))
    else:
        return word_type_list[idx]

def check_yes_no(sentence):
    is_regist = input_to_han(sentence)
    if 'y' in is_regist:
        return True
    else:
        return False

def yomi_fix(yomi, word):
    yomi_in = input(f"{word}: {''.join(yomi)}->")
    re_hiragana = re.compile(r'^[ぁ-んー]+$')
    if re_hiragana.fullmatch(yomi_in):
            return [jaconv.hira2kata(yomi_in), word]
    elif yomi_in == '':
        return
    else:
        print('type hiragana only')
        return yomi_fix(yomi, word)

def select_word_id(num, l):
    if num == '':
        return
    try:
        nums = [int(n) for n in num.split()]
        if not all([n < l for n in nums]):
            print(f'input out of index({l})')
            nums = select_word_id(input_to_han('index:'), l)

        if nums[-1] < nums[0]:
            print('input1 must be less than input2(input1, input2)')
            nums = select_word_id(input_to_han('index:'), l)
    except:
        print('input number only')
        nums = select_word_id(input_to_han('index:'), l)

    return nums

def input_to_han(stdout):
    return mojimoji.zen_to_han(input(stdout))

def extract_word_info(target_infos, idx):
    info = ''
    for target_info in target_infos:
        info += target_info[idx]
    return info

def drop_word(drop_args):
    if len(fixed_list) == 0:
        print('no words registed')
        return
    elif len(drop_args) > 2:
        print("can not drop several words.\nif you want drop word, type like this: 'drop \"idx\"'")
        return

    if len(drop_args) == 1:
        drop_idx = -1
    else:
        if abs(drop_idx) > len(fixed_list):
            print(f'out of range ({len(fixed_list)})')
            return
        drop_idx = drop_args[-1]

    do_drop = True if 'y' in input_to_han(f'{fixed_list[drop_idx]}\ndrop this?:') else False
    if do_drop:
        print('droped!!!!!!:')
        fixed_list.pop(drop_idx)
    return

def create_regist_info(word_info, w_types):
    yomi_in, word, cost, context_id = word_info
    return [
        word,
        context_id,
        context_id,
        cost,
        w_types[0],
        w_types[1],
        w_types[2],
        w_types[3],
        w_types[4],
        w_types[5],
        yomi_in,
        word,
        word,
        yomi_in,
        word,
        yomi_in,
        '固',
        '*',
        '*',
        '*',
        '*',
        '*'
    ]

def fix_dict(texts, filepath, startindex):
    v_types = verb_types()
    mecab_yomi = MeCab.Tagger('-O yomi -r /dev/null -d /usr/lib/x86_64-linux-gnu/mecab/dic/tdmelodic/')
    mecab_wakati = MeCab.Tagger('-O wakati -r /dev/null -d /usr/lib/x86_64-linux-gnu/mecab/dic/tdmelodic/')
    mecab_w_type = MeCab.Tagger('-O word -r /dev/null -d /usr/lib/x86_64-linux-gnu/mecab/dic/tdmelodic/')
    is_prev = False
    word_info_list_prev = []
    yomis_prev = ''
    wakati_prev = ''
    for text_idx, text in enumerate(texts):
        text = text.rstrip()
        words = mecab_yomi.parse(text)
        words = words.split("\n")[:-1]
        yomis = ''
        wakati = mecab_wakati.parse(text)
        sp_words = wakati.split()
        yomi_list = []
        word_info_list = []

        for (word, sp_word) in zip(words, sp_words):
            _, c_type, yomi1, yomi2, cost, context_id = word.split('\t')
            yomi = yomi1 if c_type == '固有名詞' else _ if yomi2 == '' else yomi2
            yomi = jaconv.kata2hira(yomi)
            yomis += yomi + ' '
            yomi_list.append(yomi)
            word_info_list.append([yomi,sp_word, cost, context_id])
        print(f"\ntext index is {text_idx + startindex}\n{yomis}\n{wakati}")

        while True:
            input_action = input_to_han('-----if fix yomi, type "y".-----\n')
            is_fix = True if 'y' in input_action else False
            is_next = True if input_action == '' else False

            if input_action == 'prev':
                if is_prev:
                    print('Already the previous text')
                    continue
                word_info_list_tmp = word_info_list
                word_info_list = word_info_list_prev
                is_prev = True
                print(f'\n{yomis_prev}\n{wakati_prev}')
            elif 'drop' in input_action:
                drop_word(input_action.split())
                continue

            if is_fix:
                output = [f"{str(idx)}: {y[0]}" for idx, y in enumerate(word_info_list)]
                print(' '.join(output))
                nums = select_word_id(input_to_han('index:'), len(word_info_list))
                if nums is None:
                    print(f"\n{yomis}\n{wakati}")
                    continue

                target_infos = word_info_list[nums[0]:nums[-1]+1]
                cost_extract = word_info_list[nums[0]][2]
                yomi_extract = extract_word_info(target_infos, 0)
                word_extract = extract_word_info(target_infos, 1)
                fixed_info = yomi_fix(yomi_extract, word_extract)

                if fixed_info is None:
                    print(f"\n{yomis}\n{wakati}")
                    continue

                is_overwrite = check_yes_no('overwrite this yomi?:')
                if is_overwrite:
                    # prev_word = mecab_context.parse(text)
                    # prev_word = prev_word.split('\n')[nums[0]]
                    w_types_list = mecab_w_type.parse(text).split('\n')[:-1]
                    w_types = w_types_list[nums[0]].split(',')[:6]
                    context_id_new = word_info_list[nums[0]][3]
                    cost_fixed = int(cost_extract) - 1
                else:
                    w_types, context_id_new = select_word_types(input_to_han(word_type_stdout))
                    context_id_prev = word_info_list[nums[0]-1][3] if nums[0] is not 0 else 0
                    context_id_old = word_info_list[nums[0]][3]
                    if w_types == '動詞':
                        all_verbs = v_types.all_types(fixed_info[0], fixed_info[1])
                        do_regist = check_yes_no('regist this yomi?:')
                        if do_regist:
                            for idx, verb in enumerate(all_verbs):
                                all_verbs[idx][3] = calc_cost(
                                    context_id_prev,
                                    context_id_old,
                                    verb[1],
                                    cost_extract
                                )
                            fixed_list.extend(all_verbs)
                        else:
                            print(f"\n{yomis}\n{wakati}")
                        continue

                    cost_fixed = calc_cost(
                        context_id_prev , context_id_old, context_id_new, cost_extract)
                fixed_info.extend([cost_fixed, context_id_new])

                do_regist = check_yes_no('regist this yomi?:')
                if do_regist:
                    regist_info = create_regist_info(fixed_info, w_types)
                else:
                    print(f"\n{yomis}\n{wakati}")
                    continue

                fixed_list.append(regist_info)
                print('registed!!!!!')

            elif (is_prev and is_next):
                word_info_list_prev = word_info_list
                word_info_list = word_info_list_tmp
                is_prev = False
                print(f"\n{yomis}\n{wakati}")

            elif (not is_fix and is_next):
                break

            else:
                print('invalid input')

        word_info_list_prev = word_info_list
        yomis_prev = yomis
        wakati_prev = wakati
        is_prev = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', default=None, type=str,
        help='Specify "userdict".csv path. If you update userdict, recommend to specify existing csv file')
    parser.add_argument('--startindex', default=0, type=int,
        help='Specify start row in textfile')
    parser.add_argument('--endindex', default=-1, type=int,
        help='Specify end row in textfile')
    parser.add_argument('--text', type=str, default='',
        help='Input a sentence. It can not used at the same time as --textfile')
    parser.add_argument('--textfile', type=str, default='',
        help='Input textfile. It can not used at the same time as --text')
    args = parser.parse_args()
    endindex = args.endindex + 1

    if (args.text == '') and (args.textfile == ''):
        raise ValueError('require --text or --textfile')
    elif not (args.text == '') and not (args.textfile == ''):
        raise ValueError('only one args of --text or --textfile is allowed')

    if args.text:
        texts = [args.text]

    elif args.textfile:
        if not args.textfile.split('.')[-1] == 'txt':
            raise ValueError('file extension only allows ".txt"')
        if os.path.exists(args.textfile):
            with open(args.textfile, 'r') as f:
                texts = f.readlines()
        else:
            raise ValueError(f'textfile "{args.textfile}" is not exists')

        if bool(endindex):
            texts = texts[args.startindex:endindex]
            assert texts, 'startindex must less than endindex'
        else:
            texts = texts[args.startindex:]

    try:
        fix_dict(texts, args.filepath, args.startindex)
    except Exception as e:
        print(e)
    finally:
        with open(args.filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(fixed_list)
        print(f'write {args.filepath}')

if __name__ == '__main__':
    main()
