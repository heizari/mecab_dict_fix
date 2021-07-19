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
container=tdmelodic_userdict

function remove_container {
    docker stop "$container"
}

while true; do
    [ -z "${1:-}" ] && break;
    case "$1" in
    -h) echo "
            --filepath: For all stages. Specify 'userdict'.csv path. If you update userdict, recommend to specify existing csv file.
            --startindex: For stage 0.Specify start row in textfile.
            --endindex: For stage 0. Specify end row in textfile.
            --text: For stage 1. Input a sentence. It can not used at the same time as --textfile.
            --textfile: For stage 1. Input textfile. It can not used at the same time as --text.
            --tdmelodic-dir: For stage 1. Specify tdmelodic directory if tdmelodic directory doesn't exist this directory.
            --container: For Stage 1. Specify container name.
            --stage, --stop-stage: Specify start and stop stage.
            "
        exit 1 ;;
    --*=*) echo "$0: options to scripts must be of the form --name value. need not '='"
        exit 1 ;;
    --*) name=`echo "$1" | sed s/^--// | sed s/-/_/g`;
        eval '[ -z "${'$name'+xxx}" ]' && echo "$0; invalid option $1" 1>&2 && exit 1;
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
    if [ ! -e "${dirname}/${filename}".csv ]; then
        echo No such a csv file: \'"${filepath}"\'
        exit
    fi

    if echo `docker ps -a` | grep -q "${container}"; then
        echo "\'${container}\' is already exists. Remove exists container or change container name using args --container."
        exit 1
    fi

    docker run -it --rm -d -v "${tdmelodic_dir}":/root/workspace/tdmelodic \
        -v "${dirname}":/root/output --name "${container}" tdmelodic:latest
    trap remove_container EXIT

    docker exec "${container}" python3 /root/workspace/tdmelodic/script/neologd_patch.py \
        --input /root/output/${filename}.csv \
        --output /root/output/${filename}_mod.csv
    docker exec "${container}" python3 /root/workspace/tdmelodic/nn/convert_dic.py \
        --input /root/output/${filename}_mod.csv \
        --output /root/output/${filename}_tdmelodic.csv
    sudo rm "${dirname}/${filename}"_mod.csv
fi

if [ "${stage}" -le 2 ] && [ "${stop_stage}" -ge 2 ]; then
    echo "stage 2 regist user dictionary to ${userdic}"

    if [ ! -d ${mecab}/${userdic} ]; then
        echo "make dir ${mecab}/${userdic}"
        sudo mkdir ${mecab}/${userdic}

    fi
    sudo /usr/lib/mecab/mecab-dict-index \
        -d ${mecab}/tdmelodic/ \
        -u "${mecab}/${userdic}/${filename}.dic" \
        -f  utf-8 -t utf-8 "${dirname}/${filename}_tdmelodic.csv"

    if ! grep -q "${mecab}"/"${userdic}"/"${filename}".dic "${mecab}"/tdmelodic/dicrc; then
        echo you shold add \'userdic="${mecab}"/"${userdic}"/"${filename}.dic"\' in "${mecab}/tdmelodic/dicrc"
    fi
fi
