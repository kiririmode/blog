"""はてなフォトライフへの画像のアップロードと、その URL の扱い。

フォトライフの API が返す画像 URL（`hatena:imageurl`）は、横幅 450px の縮小版 URL を指す。
元の大きさの URL は、拡張子の前に `_original` を付けた形である。
認証には環境変数 HATENA_USERNAME と HATENA_API_KEY を使う。
"""

from __future__ import annotations

import re

# フォトライフの画像 URL。stem はファイル名から拡張子を除いた部分。
FOTOLIFE_URL_PATTERN = re.compile(
    r"https?://[\w.-]*(?:st-hatena\.com|hatena\.ne\.jp)/images/fotolife/[\w./-]*?/(?P<stem>[\w-]+)\.\w+"
)


def find_shrunk_urls(text: str) -> list[str]:
    """text にあるフォトライフの URL のうち、縮小版 URL を返す。"""
    return [m.group(0) for m in FOTOLIFE_URL_PATTERN.finditer(text) if not m.group("stem").endswith("_original")]
