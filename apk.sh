# shellcheck disable=SC1113
#/bin/sh

cd "unzip目录路径"

apktool d ./"$1"

rm -rf ./"$1"