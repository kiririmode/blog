#!/usr/bin/env python3
"""Markdown 中のローカル画像参照を、はてなフォトライフの URL に置き換える。

本文に `![構成図](./xxx.svg)` のようにローカルの画像を書いておくと、
このスクリプトが次を順に実行する。

1. SVG なら resvg で PNG に変換する（PNG はそのまま使う）。
2. PNG をはてなフォトライフにアップロードする。
3. 本文の参照を `![構成図](https://cdn-ak.f.st-hatena.com/...)` に書き換える。

認証には環境変数 HATENA_USERNAME と HATENA_API_KEY を使う（.envrc が .env を読む）。

Usage:
    python3 scripts/upload_images.py <markdown> [--dry-run] [--zoom N]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

FOTOLIFE_POST_URL = "https://f.hatena.ne.jp/atom/post"
HATENA_NS = "http://www.hatena.ne.jp/info/xmlns#"

# ローカル参照だけを拾う。http(s) で始まる参照は対象外。
IMAGE_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>(?!https?://)[^)\s]+\.(?:svg|png))\)")

# resvg は文字の代替フォントに macOS の LastResort（全文字を□で描くフォント）を選ぶことがある。
# 絵文字を含む <text> 要素は、その要素全体が□になる。
# そこで LastResort を除いたフォントだけを resvg に読み込ませる。
FONT_DIRS = [
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    Path.home() / "Library/Fonts",
]
FONT_SUFFIXES = {".ttf", ".ttc", ".otf", ".otc"}


def font_args() -> list[str]:
    args = ["--skip-system-fonts"]
    for font_dir in FONT_DIRS:
        if not font_dir.is_dir():
            continue
        for font in sorted(font_dir.rglob("*")):
            if font.suffix.lower() in FONT_SUFFIXES and "LastResort" not in font.name:
                args += ["--use-font-file", str(font)]
    return args


def svg_to_png(svg: Path, zoom: float) -> Path:
    png = svg.with_suffix(".png")
    result = subprocess.run(
        ["resvg", *font_args(), "--zoom", str(zoom), str(svg), str(png)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"resvg failed for {svg}: {result.stderr.strip()}")
    for line in result.stderr.splitlines():
        # 代替フォントへの切り替えは警告として見せる。□になっていないかは目で確かめる。
        print(f"  resvg: {line}", file=sys.stderr)
    return png


def wsse_header(username: str, api_key: str) -> str:
    nonce = secrets.token_bytes(20)
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = hashlib.sha1(nonce + created.encode() + api_key.encode()).digest()
    return (
        f'UsernameToken Username="{username}", '
        f'PasswordDigest="{base64.b64encode(digest).decode()}", '
        f'Nonce="{base64.b64encode(nonce).decode()}", '
        f'Created="{created}"'
    )


def upload_to_fotolife(png: Path, title: str) -> str:
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
            "X-WSSE": wsse_header(username, api_key),
            "Content-Type": "application/xml",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            xml = response.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Fotolife upload failed: HTTP {e.code} {e.read().decode(errors='replace')}") from e

    image_url = ET.fromstring(xml).findtext(f"{{{HATENA_NS}}}imageurl")
    if not image_url:
        raise RuntimeError(f"Unexpected Fotolife response: {xml.decode(errors='replace')}")
    # imageurl は横幅 450px に縮小した画像を指す。元の大きさの画像は拡張子の前に _original が付く。
    return re.sub(r"(\.\w+)$", r"_original\1", image_url)


def process(markdown: Path, dry_run: bool, zoom: float) -> int:
    content = markdown.read_text(encoding="utf-8")
    matches = list(IMAGE_PATTERN.finditer(content))
    if not matches:
        print("No local image references found.")
        return 0

    for match in matches:
        reference = match.group(0)
        image = (markdown.parent / match.group("path")).resolve()
        if not image.exists():
            raise FileNotFoundError(f"{reference}: {image} does not exist")

        png = svg_to_png(image, zoom) if image.suffix == ".svg" else image
        print(f"{reference} -> {png}")
        if dry_run:
            continue

        image_url = upload_to_fotolife(png, png.stem)
        print(f"  uploaded: {image_url}")
        content = content.replace(reference, f"![{match.group('alt')}]({image_url})", 1)
        # 1枚ごとに書き戻し、途中で失敗しても上がった分の URL を失わない。
        markdown.write_text(content, encoding="utf-8")

    return len(matches)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="PNG への変換だけをして、アップロードと書き換えをしない")
    parser.add_argument("--zoom", type=float, default=2.0, help="SVG を PNG にするときの倍率（既定: 2）")
    args = parser.parse_args()

    try:
        process(args.markdown, args.dry_run, args.zoom)
    except Exception as e:  # noqa: BLE001 - CLI の終了コードにまとめる
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
