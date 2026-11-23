#!/usr/bin/env python3
"""下書きを公開済みエントリの形にする（公開準備）。

次を順に実行する。どこかで失敗したら、下書きを消さずに止まる。

1. front matter の `Draft` の行を消し、`Date` を日本時間の現在時刻にする。
2. 更新後の `Date` から、公開日のディレクトリ `entry/YYYYMMDD/` を決める。
3. 本文にローカルの画像参照が残っていれば、`npm run upload-images` を勧めて止まる。
4. Mermaid 図を PNG にし、フォトライフに上げ、元の大きさの URL に置き換える。
5. エントリ、Mermaid の PNG、下書き置き場の `<entry_id>-*` の付属ファイルを、公開日のディレクトリへ移す。
6. 下書きを消す。

Mermaid 図をフォトライフに上げるときは、環境変数 HATENA_USERNAME と HATENA_API_KEY を使う。

Usage:
    python3 scripts/prepare_publish.py <下書き> [--keep-date]
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import entry_files
import fotolife
import front_matter
import mermaid

# URL ではなくファイルのパスを指す画像参照
_LOCAL_IMAGE_REF = re.compile(r"!\[[^\]]*\]\((?!https?://)[^)\s]+\)")


def prepare_publish(draft: Path, keep_date: bool) -> Path:
    content, date = front_matter.publish(
        draft.read_text(encoding="utf-8"),
        None if keep_date else datetime.now(front_matter.JST),
    )
    published_dir = draft.parent.parent / date.astimezone(front_matter.JST).strftime("%Y%m%d")

    _ensure_no_local_image_refs(content, draft)

    with tempfile.TemporaryDirectory() as workdir:
        images: list[Path] = []
        if mermaid.has_diagrams(content):
            content, images = mermaid.render(content, draft.name, Path(workdir))
            for image in images:
                url = fotolife.upload_png(image, image.stem)
                print(f"uploaded: {image.name} -> {url}")
                content = content.replace(f"![diagram](./{image.name})", f"![diagram]({url})")
            if _LOCAL_IMAGE_REF.search(content):
                raise RuntimeError("Mermaid 図の PNG の一部が、フォトライフの URL に置き換わりませんでした")
        return entry_files.move_to_published_dir(draft, content, images, published_dir)


def _ensure_no_local_image_refs(content: str, draft: Path) -> None:
    local_refs = _LOCAL_IMAGE_REF.findall(content)
    if local_refs:
        raise RuntimeError(
            "本文にローカルの画像参照が残っています。"
            f"先に npm run upload-images {draft} でフォトライフに上げてください: " + ", ".join(local_refs)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft", type=Path, help="下書き置き場にある下書きの Markdown")
    parser.add_argument("--keep-date", action="store_true", help="Date を変えない。公開日のディレクトリは今の Date から決める")
    args = parser.parse_args()

    try:
        entry = prepare_publish(args.draft, args.keep_date)
    except Exception as e:  # noqa: BLE001 - CLI の終了コードにまとめる
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"公開準備が終わりました: {entry}")


if __name__ == "__main__":
    main()
