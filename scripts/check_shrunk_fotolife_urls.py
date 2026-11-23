#!/usr/bin/env python3
"""エントリの本文にある、フォトライフの縮小版 URL を報告する。

フォトライフの URL のうち、ファイル名が `_original` 版でないものを縮小版 URL とみなす。
縮小版 URL は横幅 450px の画像を指すので、拡張子の前に `_original` を付けた
元の大きさの URL に直す。違反があれば、ファイル名、行番号、URL を標準エラーに出し、
終了コード 1 で終わる。

Usage:
    python3 scripts/check_shrunk_fotolife_urls.py <markdown>...
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fotolife import find_shrunk_urls


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("markdown", type=Path, nargs="+")
    args = parser.parse_args()

    found = False
    for markdown in args.markdown:
        lines = markdown.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            for url in find_shrunk_urls(line):
                found = True
                print(f"{markdown}:{line_number}: 縮小版 URL です。_original 版に直してください: {url}", file=sys.stderr)
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
