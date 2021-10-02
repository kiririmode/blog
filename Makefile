BLOG = kiririmode.hatenablog.jp

.PHONY: pull
pull:
	blogsync pull ${BLOG}

.PHONY: new-entry
new-entry:
	echo | blogsync post --draft ${BLOG} | tail -1 | awk '{ print $1 }' | pbcopy

.PHONY: check
check:
	scripts/check.sh

.PHONY: post
post: check
	scripts/publish.sh

.PHONY: clean
clean:
	find ${BLOG} -size 0 -name '*.md' -print0 | xargs -0 rm
