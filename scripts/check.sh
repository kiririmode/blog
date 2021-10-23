#!/bin/bash
set -eux

TIMESTAMP_FILE="last_publish_time"

function check {
    local entries=$(git log --name-only --pretty="tformat:" --since $(cat $TIMESTAMP_FILE) -- kiririmode.hatenablog.jp/entry/)

    if [[ -n $entries ]]; then
        npx textlint $entries
    fi
}

check
