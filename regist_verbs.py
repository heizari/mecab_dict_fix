import pdb
import jaconv
import csv
class verb_types:
    def __init__(self):
        self.char_A = ['ア','カ','ガ','サ','ザ','タ','ダ','ナ','ハ','バ','パ','マ','ヤ','ラ','ワ']
        self.char_I = ['イ','キ','ギ','シ','ジ','チ','ヂ','ニ','ヒ','ビ','ピ','ミ','ー','リ','イ']
        self.char_U = ['ウ','ク','グ','ス','ズ','ツ','ヅ','ヌ','フ','ブ','プ','ム','ユ','ル','ウ']
        self.char_E = ['エ','ケ','ゲ','セ','ゼ','テ','デ','ネ','ヘ','ベ','ペ','メ','ー','レ','エ']
        self.char_O = ['オ','コ','ゴ','ソ','ゾ','ト','ド','ノ','ホ','ボ','ポ','モ','ヨ','ロ','オ']
        self.char_T = ["ッ","ッ"]
        with open('id.csv') as f:
            reader = csv.reader(f)
            self.context_id = [l for l in reader]
        # pdb.set_trace()

    def append_dict(self, word, w_type, katsuyou, trans_type, yomi):
        cid = 0
        if katsuyou == '五段-ワ行':
            katsuyou = '五段-ワア行'
        for idx, types in enumerate(self.context_id):
            if types[4] == katsuyou and types[5].split('-')[0] == trans_type:
                trans_type = types[5]
                cid = idx + 1
                break
        if cid == 0:
            return
        self.wordDic.append([
            word,
            cid,
            cid,
            '*',
            w_type,
            '一般',
            '*',
            '*',
            katsuyou,
            trans_type,
            self.yomi,
            self.word,
            word,
            yomi,
            self.word,
            self.yomi,
            '和',
            '*',
            '*',
            '*',
            '*',
            '*'
        ])

    def word_init(self):
        self.wordDic = []
        self.word = ''
        self.word_br = ''
        self.word_bs = ''
        self.word_gc = ''
        self.word_gp = ''
        self.yomi = '*'
        self.yomi_br = '*'
        self.yomi_bs = '*'
        self.yomi_gp = '*'
        self.dan = ''
        self.num_X = -1
        self.num_Y = -1
        self.num_Z = -1

    def all_types(self,yomi, word):
        self.word_init()
        # 入力単語
        self.word = word
        self.word_br = word[:-1]
        self.word_bs = word[:-2]
        self.word_gc = word[-1:]
        self.word_gp = word[-2:-1]

        # 読み仮名
        if yomi != '*':
            yomi = jaconv.hira2kata(yomi)
            self.yomi = yomi
            self.yomi_br = yomi[:-1]
            self.yomi_bs = yomi[:-2]
            self.yomi_gp = yomi[-2:-1]
            print(self.yomi_gp)
        # pdb.set_trace()

        for n in range(0, 15):
            if self.word_gc == jaconv.kata2hira(self.char_U[n]):
                self.num_X = n
            if self.yomi_gp == self.char_I[n]:
                self.num_Y = n
                self.dan = '上'
            elif self.yomi_gp == self.char_E[n]:
                self.num_Y = n
                self.dan = '下'
            elif (self.word_gp == self.char_E[n] or self.word_gp == self.char_I[n]):
                self.num_Z = n
        print(f'x:{self.num_X}, y:{self.num_Y}')

        if word == '来る' or word == 'くる':
            print('カ変変格活用')
        elif self.word_gp == 'す' and self.word_gc == 'る':
            print ('さ行変格活用')
            # self.append_dict(word, '動詞', 'サ変', '基本形', yomi)
            self.append_dict(self.word_bs+'さ', '動詞', 'サ変', '未然形', self.yomi_bs+'サ')
            self.append_dict(self.word_bs+'し', '動詞', 'サ変', '未然形', self.yomi_bs+'シ')
            self.append_dict(self.word_bs+'せ', '動詞', 'サ変', '未然形', self.yomi_bs+'セ')
            self.append_dict(self.word_bs+'し', '動詞', 'サ変', '連用形', self.yomi_bs+'シ')
            self.append_dict(self.word_bs+'する', '動詞', 'サ変', '終止形',self.yomi_bs+'スル')
            self.append_dict(self.word_bs+'する', '動詞', 'サ変', '連体形',self.yomi_bs+'スル')
            self.append_dict(self.word_bs+'すれ', '動詞', 'サ変', '仮定形',self.yomi_bs+'スレ')
            self.append_dict(self.word_bs+'しろ', '動詞', 'サ変', '命令形',self.yomi_bs+'シロ')
            self.append_dict(self.word_bs+'せよ', '動詞', 'サ変', '命令形',self.yomi_bs+'セヨ')
            # self.append_dict(self.word_bs+'せる', '動詞', 'サ変', '可能動詞',self.yomi_bs+'セル')
        elif (self.word_gp == 'じ' or self.word_gp == 'ず') and self.word_gp == 'る':
            print ('ざ行変格活用')
            # self.append_dict(word, '動詞', 'ザ変', '基本形',yomi)
            self.append_dict(self.word_bs+'じ','動詞','ザ変','未然形',self.yomi_bs+'ジ')
            self.append_dict(self.word_bs+'ぜ','動詞','ザ変','未然形',self.yomi_bs+'ゼ')
            self.append_dict(self.word_bs+'じ','動詞','ザ変','連用形',self.yomi_bs+'ジ')
            self.append_dict(self.word_bs+'じる','動詞','ザ変','終止形',self.yomi_bs+'ジル')
            self.append_dict(self.word_bs+'ずる','動詞','ザ変','終止形',self.yomi_bs+'ズル')
            self.append_dict(self.word_bs+'じる','動詞','ザ変','連体形',self.yomi_bs+'ジル')
            self.append_dict(self.word_bs+'ずる','動詞','ザ変','連体形',self.yomi_bs+'ズル')
            self.append_dict(self.word_bs+'じれ','動詞','ザ変','仮定形',self.yomi_bs+'ジレ')
            self.append_dict(self.word_bs+'ずれ','動詞','ザ変','仮定形',self.yomi_bs+'ズレ')
            self.append_dict(self.word_bs+'じろ','動詞','ザ変','命令形',self.yomi_bs+'ジロ')
            self.append_dict(self.word_bs+'ぜよ','動詞','ザ変','命令形',self.yomi_bs+'ゼヨ')
            # self.append_dict(self.word_bs+'ぜる','動詞','ザ変','可能動詞',self.yomi_bs+'ゼル')
        elif word == '行く' or word == 'いく' or word == 'ける' or word == '競る' or word == 'てる':
            print ('五段')
            self.append_dict(self.word_br+'っ', '動詞',f'五段-{self.char_A[self.num_X]}行','連用形',self.yomi_br+'ッ')
            self.KatuyouGodan()
        elif (word=="居る" or word=="鋳る" or word=="射る" or word=="着る" or word=="似る" or  word=="見る" or word=="得る" or word=="出る" or word=="経る" or word=="寝る"):
            m = self.char_A[self.num_Y]
            self.char_A[self.num_Y] = 'O'
            self.KatuyouIchidan()
            self.char_A[self.num_Y] = m
        elif self.word_gc == 'る' and self.num_Z >= 0:
            self.KatuyouIchidan()
        elif word == 'ぬ':
            print ('打ち消し助動詞')
            # self.append_dict(word, '打消助動詞', '*','基本形',yomi)
            self.append_dict('ず','打消助動詞','*', '連用形','ズ')
            self.append_dict('ぬ','打消助動詞','*', '終止形','ヌ')
            self.append_dict('ん','打消助動詞','*', '終止形','ン')
            self.append_dict('ぬ','打消助動詞','*', '連体形','ヌ')
            self.append_dict('ん','打消助動詞','*', '連体形','ン')
            self.append_dict('ね','打消助動詞','*', '仮定形','ネ')
        elif word == 'う' or word == 'よぅ' or word == 'まい':
            print ('意思助動詞系')
            # self.append_dict(word,'意志助動詞','*','基本形', yomi)
            self.append_dict(word,'意志助動詞','*','終止形', yomi)
            self.append_dict(word,'意志助動詞','*','連体形', yomi)
        elif word == 'です' or word == 'ます':
            print ('丁寧助動詞系')
            # self.append_dict(word, '丁寧動詞','*', '基本形', yomi)
            self.append_dict(self.word_br+'しょ', '丁寧動詞','*','未然形',self.yomi_br+'ショ')
            self.append_dict(self.word_br+'し', '丁寧動詞','*','連用形',self.yomi_br+'シ')
            self.append_dict(self.word_br+'す','丁寧動詞','*','終止形',self.yomi_br+'ス')
        elif self.num_X >= 0:
            if self.char_A[self.num_X] == 'ア' or self.char_A[self.num_X] == 'タ' or self.char_A[self.num_X] == 'ラ' or self.char_A[self.num_X] == 'ワ':
                print ('五段')
                self.append_dict(self.word_br+'っ', '動詞','五段-'+self.char_A[self.num_X]+'行', '連用形',self.yomi_br+'ッ')
                self.KatuyouGodan()
            elif self.char_A[self.num_X] == 'マ' or self.char_A[self.num_X] == 'ハ' or self.char_A[self.num_X] == 'ナ':
                print ('五段')
                self.append_dict(self.word_br+'ん','動詞','五段-'+self.char_A[self.num_X]+'行','連用形',self.yomi_br+'ン')
                self.KatuyouGodan()
            elif self.char_A[self.num_X] == 'カ' or self.char_A[self.num_X] == 'ガ':
                print ('五段')
                self.append_dict(self.word_br+'い', '動詞','五段-'+self.char_A[self.num_X]+'行', '連用形',self.yomi_br+'イ')
                self.KatuyouGodan()
            elif self.char_A[self.num_X] == 'サ':
                print ('五段')
                self.append_dict(self.word_br+self.char_I[self.num_X],'動詞','五段-'+self.char_A[self.num_X]+'行','連用形',self.yomi_br+self.char_I[self.num_X])
                self.KatuyouGodan()
        elif self.word_gc == 'い':
            print ('形容詞活用')
            # self.append_dict(word,'形容詞','*', '基本形',yomi)
            self.append_dict(self.word_br+'く','形容詞','*','未然形',self.yomi_br+'ク')
            self.append_dict(self.word_br+'かろ','形容詞','*','未然形',self.yomi_br+'カロ')
            self.append_dict(self.word_br+'く', '形容詞','*', '連用形',self.yomi_br+'ク')
            self.append_dict(self.word_br+'かっ', '形容詞','*', '連用形',self.yomi_br+'カッ')
            self.append_dict(self.word_br+'い', '形容詞','*','終止形',self.yomi_br+'イ')
            self.append_dict(self.word_br+'い', '形容詞','*','連体形',self.yomi_br+'イ')
            self.append_dict(self.word_br+'けれ', '形容詞','*', '仮定形',self.yomi_br+'ケレ')
        elif self.word_gc == 'だ':
            print ('形容動詞系')
            # self.append_dict(word,'形容動詞','基本形',yomi)
            self.append_dict(self.word_br+'で', '形容動詞','*','未然形',self.yomi_br+'デ')
            self.append_dict(self.word_br+'だろ','形容動詞','*','未然形',self.yomi_br+'ダロ')
            self.append_dict(self.word_br+'で', '形容動詞','*','連用形',self.yomi_br+'デ')
            self.append_dict(self.word_br+'だっ','形容動詞','*','連用形',self.yomi_br+'ダッ')
            self.append_dict(self.word_br+'に', '形容動詞','*','連用形',self.yomi_br+'ニ')
            self.append_dict(self.word_br+'だ', '形容動詞','*','終止形',self.yomi_br+'ダ')
            self.append_dict(self.word_br+'だ', '形容動詞','*','連体形',self.yomi_br+'ナ')
            self.append_dict(self.word_br+'なら','形容動詞','*','仮定形',self.yomi_br+'ナラ')
        else:
            print ('can not regist verbs')
        return self.wordDic

    def KatuyouIchidan(self):
        # self.append_dict(self.word,'動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','基本形',self.yomi)
        self.append_dict(self.word_br,'動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','未然形',self.yomi_br)
        self.append_dict(self.word_br,'動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','連用形',self.yomi_br)
        self.append_dict(self.word_br+'る','動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','終止形',self.yomi_br+'ル')
        self.append_dict(self.word_br+'る','動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','連体形',self.yomi_br+'ル')
        self.append_dict(self.word_br+'れ','動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','仮定形',self.yomi_br+'レ')
        self.append_dict(self.word_br+'ろ','動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','命令形',self.yomi_br+'ロ')
        self.append_dict(self.word_br+'よ','動詞',self.dan+'一段-'+self.char_A[self.num_Y]+'行','命令形',self.yomi_br+'ヨ')

    def KatuyouGodan(self):
        A = jaconv.kata2hira(self.char_A[self.num_X])
        I = jaconv.kata2hira(self.char_I[self.num_X])
        U = jaconv.kata2hira(self.char_U[self.num_X])
        E = jaconv.kata2hira(self.char_E[self.num_X])
        O = jaconv.kata2hira(self.char_O[self.num_X])
        # self.append_dict(self.word,'動詞','五段-'+self.char_A[self.num_X]+'行','基本形',self.yomi)
        self.append_dict(self.word_br+A,'動詞','五段-'+self.char_A[self.num_X]+'行','未然形',self.yomi_br+self.char_A[self.num_X])
        self.append_dict(self.word_br+O,'動詞','五段-'+self.char_A[self.num_X]+'行','未然形',self.yomi_br+self.char_O[self.num_X])
        self.append_dict(self.word_br+I,'動詞','五段-'+self.char_A[self.num_X]+'行','連用形',self.yomi_br+self.char_I[self.num_X])
        self.append_dict(self.word_br+U,'動詞','五段-'+self.char_A[self.num_X]+'行','終止形',self.yomi_br+self.char_U[self.num_X])
        self.append_dict(self.word_br+U,'動詞','五段-'+self.char_A[self.num_X]+'行','連体形',self.yomi_br+self.char_U[self.num_X])
        self.append_dict(self.word_br+E,'動詞','五段-'+self.char_A[self.num_X]+'行','仮定形',self.yomi_br+self.char_E[self.num_X])
        self.append_dict(self.word_br+E,'動詞','五段-'+self.char_A[self.num_X]+'行','命令形',self.yomi_br+self.char_E[self.num_X])
        # self.append_dict(self.word_br+E,'動詞','五段-'+self.char_A[self.num_X]+'行','可能動詞',self.yomi_br+self.char_E[self.num_X])

if __name__ == '__main__':
    w = verb_types()
    while True:
        word = input('INPUT WORD (finish = n) :')
        yomi = input('yomi :')
        if word == 'n' or yomi == 'n':
            break
        for k in w.all_types(yomi, word):
            print(k)