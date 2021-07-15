#!/bin/bash
set -e
mecab=`mecab-config --dicdir`
filepath=`pwd`/add_dict.csv
userdic=userdic
startindex=0
endindex=-1
stage=0
stop_stage=100
textfile=''
text=''
tdmelodic_dir=`pwd`/tdmelodic

while true; do
    [ -z "${1:-}" ] && break;
    case "$1" in
    -h) echo "--filepath: Using all stages. Specify 'userdict'.csv path. If you update userdict, recommend to specify existing csv file\
              --startindex: Using stage 0.Specify start row in textfile\
              --endindex: Using stage 0. Specify end row in textfile\
              --text: Input a sentence. It can not used at the same time as --textfile\
              --textfile: Input textfile. It can not used at the same time as --text\
              --tdmelodic-dir: Specify tdmelodic directory if tdmelodic directory is not in this directory\
              --stage, --stop-stage: Specify start and stop stage"
    --*=*) echo "$0: options to scripts must be of the form --name value. need not '='"
        exit 1 ;;
    --*) name=`echo "$1" | sed s/^--// | sed s/-/_/g`;
        eval '[ -z "${'$name'+xxx}" ]' && echo '$0; invalid option $1' 1>&2 && exit 1;
        eval $name=\"$2\";
        shift 2;
    esac
done

echo "${textfile}"
tdmelodic_dir=`realpath "${tdmelodic_dir}"`
filepath=`realpath "${filepath}"`
dirname=${filepath%/*}
filename=${filepath##*/}
filename=${filename%.*}

if [ "${stage}" -le 0 ] && [ "${stop_stage}" -ge 0 ]; then
    echo "stage 0 create user dictionary as ${filename}.csv"
    if [ "${endindex}" -eq 0 ]; then
        python regist_userdict.py \
        --filepath "${filepath}" \
        --startindex "${startindex}" \
        --text "${text}" \
        --textfile "${textfile}"
    else
        python regist_userdict.py \
        --filepath "${filepath}" \
        --startindex "${startindex}" \
        --text "${text}" \
        --endindex ${endindex} \
        --textfile "${textfile}"
    fi
fi

if [ "${stage}" -le 1 ] && [ "${stop_stage}" -ge 1 ]; then
    echo 'stage 1 inference accents'
    docker run -it --rm -d -v "${tdmelodic_dir}":/root/workspace/tdmelodic \
        -v "${dirname}":/root/output --name tdm tdmelodic:latest
    docker exec tdm python3 /root/workspace/tdmelodic/script/neologd_patch.py \
        --input /root/output/${filename}.csv \
        --output /root/output/${filename}_mod.csv
    docker exec tdm python3 /root/workspace/tdmelodic/nn/convert_dic.py \
        --input /root/output/${filename}_mod.csv \
        --output /root/output/${filename}_tdmelodic.csv
    sudo rm "${filename}"_mod.csv
    docker stop tdm
fi

if [ "${stage}" -le 2 ] && [ "${stop_stage}" -ge 2 ]; then
    echo "stage 2 regist user dictionary to ${userdic}"

    if [ ! -d ${mecab}/${userdic} ]; then
        sudo mkdir ${mecab}/${userdic}
        echo "make dir ${mecab}/${userdic}"
    fi
    sudo /usr/lib/mecab/mecab-dict-index \
        -d ${mecab}/tdmelodic/ \
        -u "${mecab}/${userdic}/${filename}.dic" \
        -f  utf-8 -t utf-8 "${dirname}/${filename}_tdmelodic.csv"
fi