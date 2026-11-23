"""下書きと付属ファイルを、公開日のディレクトリへ移す。

付属ファイルは、下書き置き場にある `<entry_id>-` で始まるファイルである。
"""

from __future__ import annotations

import shutil
from pathlib import Path


def move_to_published_dir(draft: Path, content: str, mermaid_pngs: list[Path], published_dir: Path) -> Path:
    """下書きを公開日のディレクトリへ移し、公開済みエントリのパスを返す。

    公開済みエントリには content を書く。mermaid_pngs（Mermaid 図から作った PNG）はそのディレクトリへ写す。
    付属ファイルもそのディレクトリへ移す。最後に下書きを消す。
    """
    published_dir.mkdir(parents=True, exist_ok=True)
    entry = published_dir / draft.name
    entry.write_text(content, encoding="utf-8")
    for png in mermaid_pngs:
        shutil.copy2(png, published_dir / png.name)
    for attached in sorted(draft.parent.glob(f"{draft.stem}-*")):
        shutil.move(attached, published_dir / attached.name)
    draft.unlink()
    return entry
