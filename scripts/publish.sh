#!/bin/bash
set -eux

TIMESTAMP_FILE="last_publish_time"

function publish {
    local entries=$(git log --name-only --pretty="tformat:" --since $(cat $TIMESTAMP_FILE) -- kiririmode.hatenablog.jp/entry/)

    blogsync push $entries &&
        date -u +%s >$TIMESTAMP_FILE

    if [[ -n ${GITHUB_ACTIONS-} ]]; then
        git config --global user.email "kiririmode@gmail.com"
        git config --global user.name $GITHUB_ACTOR
    fi
    git add $TIMESTAMP_FILE &&
        git commit --message "update: last_publish_time" &&
        git push origin master
}

publish
