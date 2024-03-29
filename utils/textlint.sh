#!/bin/bash
set -eu
shopt -s nullglob dotglob

# textlint 対象を現在日から何日前にするか
readonly LINT_TARGET_DAYS=5

for i in $(seq "$LINT_TARGET_DAYS" -1 0); do
    dateDir=$(date +%Y%m%d --date "$i days ago")

    # Markdownファイルが存在しなければ、次のディレクトリに処理を移す
    for f in kiririmode.hatenablog.jp/entry/"${dateDir}"/*.md; do
        npx textlint --format checkstyle "$f" |
            reviewdog \
                -f=checkstyle \
                -name="textlint" \
                -reporter=github-pr-review \
                -fail-on-error=true
    done

done
