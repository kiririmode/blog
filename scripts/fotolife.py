"""はてなフォトライフへの画像のアップロードと、その URL の扱い。

フォトライフの API が返す画像 URL（`hatena:imageurl`）は、横幅 450px の縮小版 URL を指す。
元の大きさの URL は、拡張子の前に `_original` を付けた形である。
本文には元の大きさの URL を書く（docs/adr/0003）。
認証には環境変数 HATENA_USERNAME と HATENA_API_KEY を使う。
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
import secrets
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

FOTOLIFE_POST_URL = "https://f.hatena.ne.jp/atom/post"
HATENA_NS = "http://www.hatena.ne.jp/info/xmlns#"

# フォトライフの画像 URL。stem はファイル名から拡張子を除いた部分。
FOTOLIFE_URL_PATTERN = re.compile(
    r"https?://[\w.-]*(?:st-hatena\.com|hatena\.ne\.jp)/images/fotolife/[\w./-]*?/(?P<stem>[\w-]+)\.\w+"
)


def find_shrunk_urls(text: str) -> list[str]:
    """text にあるフォトライフの URL のうち、縮小版 URL を返す。"""
    return [m.group(0) for m in FOTOLIFE_URL_PATTERN.finditer(text) if not m.group("stem").endswith("_original")]


def to_original_url(shrunk_url: str) -> str:
    """縮小版 URL を元の大きさの URL にする。"""
    return re.sub(r"(\.\w+)$", r"_original\1", shrunk_url)


def upload_png(png: Path, title: str) -> str:
    """PNG をフォトライフにアップロードし、元の大きさの URL を返す。"""
    username = os.environ.get("HATENA_USERNAME")
    api_key = os.environ.get("HATENA_API_KEY")
    if not username or not api_key:
        raise RuntimeError("HATENA_USERNAME and HATENA_API_KEY environment variables are required")

    body = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<entry xmlns="http://purl.org/atom/ns#">'
        f"<title>{escape(title)}</title>"
        f'<content mode="base64" type="image/png">{base64.b64encode(png.read_bytes()).decode()}</content>'
        "</entry>"
    ).encode()
    request = urllib.request.Request(
        FOTOLIFE_POST_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": 'WSSE profile="UsernameToken"',
            "X-WSSE": _wsse_header(username, api_key),
            "Content-Type": "application/xml",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            xml = response.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"フォトライフへのアップロードに失敗しました: HTTP {e.code} {e.read().decode(errors='replace')}") from e

    image_url = ET.fromstring(xml).findtext(f"{{{HATENA_NS}}}imageurl")
    if not image_url:
        raise RuntimeError(f"フォトライフの応答に画像 URL がありません: {xml.decode(errors='replace')}")
    return to_original_url(image_url)


def _wsse_header(username: str, api_key: str) -> str:
    nonce = secrets.token_bytes(20)
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = hashlib.sha1(nonce + created.encode() + api_key.encode()).digest()
    return (
        f'UsernameToken Username="{username}", '
        f'PasswordDigest="{base64.b64encode(digest).decode()}", '
        f'Nonce="{base64.b64encode(nonce).decode()}", '
        f'Created="{created}"'
    )
