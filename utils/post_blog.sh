#!/bin/bash
set -eu

# 投稿対象を現在日から何日前にするか
readonly POST_TARGET_DAYS=5

for i in $(seq "$POST_TARGET_DAYS" -1 0); do
    dateDir=$(date +%Y%m%d --date "$i days ago")

    # Markdownファイルが存在しなければ、次のディレクトリに処理を移す
    mdfiles=(kiririmode.hatenablog.jp/entry/"${dateDir}"/*.md)
    if [[ -z ${#mdfiles} ]]; then
        continue
    fi

    echo "target: ${mdfiles[*]}"
    bin/blogsync push "${mdfiles[*]}"
done
