"""本文の Mermaid 図を、mermaid-cli（mmdc）と Chrome で PNG にする。"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import NamedTuple

PUPPETEER_CONFIG = Path(__file__).resolve().parent.parent / "puppeteer-config.json"

_MERMAID_FENCE = re.compile(r"^```mermaid\s*$", re.MULTILINE)

# 先頭ほど優先する。壊れた候補（Homebrew のラッパーだけが残っている等）は飛ばす。
_CHROME_CANDIDATES = [
    "/opt/homebrew/bin/chromium",
    "/usr/local/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


class RenderedDiagram(NamedTuple):
    """PNG にした Mermaid 図と、本文でそれを指すローカルの画像参照。"""

    png: Path
    reference: str


def has_diagrams(content: str) -> bool:
    return bool(_MERMAID_FENCE.search(content))


def render(content: str, name: str, workdir: Path) -> tuple[str, list[RenderedDiagram]]:
    """Mermaid 図を PNG にし、図を PNG への参照に置き換えた本文と、PNG ごとの参照を返す。

    PNG は workdir に `<name の stem>-<連番>.png` として書く。
    """
    markdown = workdir / name
    markdown.write_text(content, encoding="utf-8")
    config = workdir / "puppeteer-config.json"
    base_config = json.loads(PUPPETEER_CONFIG.read_text(encoding="utf-8"))
    config.write_text(json.dumps({**base_config, "executablePath": _chrome_executable()}), encoding="utf-8")

    result = subprocess.run(
        ["npx", "-y", "mmdc", "-i", str(markdown), "-o", str(markdown), "-e", "png", "-p", str(config)],
        capture_output=True,
        text=True,
        cwd=PUPPETEER_CONFIG.parent,
    )
    converted = markdown.read_text(encoding="utf-8")
    if result.returncode != 0 or has_diagrams(converted):
        raise RuntimeError(f"Mermaid 図を PNG にできませんでした: {result.stderr.strip() or result.stdout.strip()}")
    # mmdc は図を `![diagram](./<PNG のファイル名>)` に置き換える。
    pngs = sorted(workdir.glob(f"{markdown.stem}-*.png"))
    return converted, [RenderedDiagram(png, f"![diagram](./{png.name})") for png in pngs]


def _chrome_executable() -> str:
    candidates = [os.environ.get("PUPPETEER_EXECUTABLE_PATH"), *_CHROME_CANDIDATES]
    for candidate in filter(None, candidates):
        if not Path(candidate).exists():
            continue
        try:
            subprocess.run([candidate, "--version"], capture_output=True, check=True)
        except (OSError, subprocess.CalledProcessError):
            continue
        return candidate
    raise RuntimeError(
        "No working Chrome/Chromium executable found. "
        "Install Google Chrome or Chromium, or set PUPPETEER_EXECUTABLE_PATH."
    )
