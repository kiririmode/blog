BLOG = kiririmode.hatenablog.jp
TARGETS = $(shell git log -1 --name-only --pretty=oneline --full-index -- kiririmode.hatenablog.jp/entry/ | grep -vE '^[0-9a-f]{40}' | sort -u | grep '.md$$')

.PHONY: pull
pull:
	blogsync pull ${BLOG}

.PHONY: new-entry
new-entry:
	echo | blogsync post --draft ${BLOG} | tail -1 | awk '{ print $1 }' | pbcopy

.PHONY: check
check:
	npx textlint ${TARGETS}

.PHONY: post
post: check
	echo ${TARGETS} | xargs -n1 blogsync push

.PHONY: clean
clean:
	find ${BLOG} -size 0 -name '*.md' -print0 | xargs -0 rm
