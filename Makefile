BLOG = kiririmode.hatenablog.jp
DATE = $(shell date +%Y%m%d)

.PHONY: pull
pull:
	blogsync pull ${BLOG}

.PHONY: new-entry
new-entry:
	echo | blogsync post --draft ${BLOG} | tail -1 | awk '{ print $1 }' | pbcopy

.PHONY: check
check:
	npx textlint --fix ${BLOG}/entry/${DATE}/*.md
	npx textlint ${BLOG}/entry/${DATE}/*.md

.PHONY: post
post: check
	blogsync push ${BLOG}/entry/${DATE}/*.md

.PHONY: clean
clean:
	find ${BLOG} -size 0 -name '*.md' -print0 | xargs -0 rm
