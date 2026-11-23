"""本文にあるローカルの画像参照を見つけ、URL の参照に書き換える。

ローカルの画像参照は、URL ではなくファイルのパスを指す画像参照（`![alt](./x.svg)` など）である。
拡張子は問わない。フェンスで囲んだコードブロック（``` や ~~~）の中にあるものは、
Markdown の書き方を説明する例なので数えない。
"""

from __future__ import annotations

import re

_REFERENCE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>(?!https?://)[^)\s]+)\)")

# 閉じるフェンスがなければ、本文の最後までをコードブロックとみなす（CommonMark と同じ）。
_FENCED_CODE_BLOCK = re.compile(
    r"^ {0,3}(?P<fence>`{3,}|~{3,})[^\n]*\n.*?(?:^ {0,3}(?P=fence)(?:`*|~*)[ \t]*$|\Z)",
    re.MULTILINE | re.DOTALL,
)


def find(content: str) -> list[re.Match[str]]:
    """content にあるローカルの画像参照を、出てくる順に返す。

    各 Match の group("alt") は代替テキスト、group("path") は画像のパスである。
    """
    code_blocks = [m.span() for m in _FENCED_CODE_BLOCK.finditer(content)]
    return [
        m for m in _REFERENCE.finditer(content)
        if not any(start <= m.start() < end for start, end in code_blocks)
    ]


def with_url(reference: str, url: str) -> str:
    """ローカルの画像参照 reference を、代替テキストを保ったまま url を指す参照にする。"""
    match = _REFERENCE.fullmatch(reference)
    if not match:
        raise ValueError(f"ローカルの画像参照ではありません: {reference}")
    return f"![{match.group('alt')}]({url})"
