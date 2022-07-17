#!/bin/zsh
folder =  /Users/lll/Music/网易云音乐/

cd "$(dirname "$(greadlink -f "$0")")"

./ncmdump $folder
