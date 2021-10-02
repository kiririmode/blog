#!/bin/bash
set -eux

TIMESTAMP_FILE="last_publish_time"

function check {
    local entries=$(git log --name-only --pretty="tformat:" --since $(cat $TIMESTAMP_FILE) -- kiririmode.hatenablog.jp/entry/)

    npx textlint $entries
}

check
