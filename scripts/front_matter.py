"""公開準備での front matter の更新。

書き換えるのは `Draft` の行と `Date` の行だけである。他の行は、並び順も書式も変えない。
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))

_FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?\n)---\n", re.DOTALL)
_DATE_LINE = re.compile(r"^Date:[ \t]*(?P<value>.*)$", re.MULTILINE)
_DRAFT_LINE = re.compile(r"^Draft:.*\n", re.MULTILINE)


class MissingDateError(ValueError):
    """Date を保とうとしたが、front matter に Date がない。"""


def publish(content: str, now: datetime | None) -> tuple[str, datetime]:
    """下書きの content を公開済みエントリの形にし、その Date とともに返す。

    `Draft` の行を消す。now を渡したときは `Date` を now にし、None のときは `Date` を保つ。
    保った `Date` にタイムゾーンがなければ、ブログのタイムゾーンである日本時間とみなす。
    """
    match = _FRONT_MATTER.match(content)
    if not match:
        raise ValueError("front matter が見つかりません（先頭が --- で始まっていません）")
    front_matter = _DRAFT_LINE.sub("", match.group("body"))

    if now is None:
        date_match = _DATE_LINE.search(front_matter)
        if not date_match:
            raise MissingDateError("front matter に Date がありません")
        try:
            date = datetime.fromisoformat(date_match.group("value").strip())
        except ValueError as e:
            raise ValueError(f"Date の形式が読めません: {date_match.group('value')}") from e
        if date.tzinfo is None:
            date = date.replace(tzinfo=JST)
    else:
        date = now.astimezone(JST).replace(microsecond=0)
        date_line = f"Date: {date.isoformat()}"
        if _DATE_LINE.search(front_matter):
            front_matter = _DATE_LINE.sub(lambda _: date_line, front_matter, count=1)
        else:
            front_matter += date_line + "\n"

    return f"---\n{front_matter}---\n" + content[match.end():], date
