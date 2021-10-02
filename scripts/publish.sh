#!/bin/bash
set -eux

TIMESTAMP_FILE="last_publish_time"

function publish {
    local entries=$(git log --name-only --pretty="tformat:" --since $(cat $TIMESTAMP_FILE) -- kiririmode.hatenablog.jp/entry/)

    blogsync push $entries &&
        date -u +%s >$TIMESTAMP_FILE
    git add $TIMESTAMP_FILE &&
        git commit --message "update: last_publish_time" &&
        git push origin master
}

publish
