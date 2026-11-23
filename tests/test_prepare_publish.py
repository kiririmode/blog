"""公開準備の CLI を、出力されたファイルの配置と中身、終了コード、標準エラーで確かめる。

下書きには Mermaid 図を入れない。こうして Chrome とフォトライフなしで動かす。
誤ってアップロードしないよう、HATENA_ で始まる環境変数を外して CLI を走らせる。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

CLI = Path(__file__).resolve().parent.parent / "scripts" / "prepare_publish.py"
JST = timezone(timedelta(hours=9))

ENTRY_ID = "6802418398"

FRONT_MATTER_BEFORE_DATE = """\
Title: テストのエントリ
Category:
- generative ai
- claude-code
"""
FRONT_MATTER_AFTER_DRAFT = """\
EditURL: https://blog.hatena.ne.jp/kiririmode/kiririmode.hatenablog.jp/atom/entry/6802418398
PreviewURL: https://kiririmode.hatenablog.jp/draft/entry/abcdefg
"""
BODY = """\

本文の1行目。

## 見出し

![外部の画像](https://example.com/image.png)
"""


def draft_text(date: str = "2020-01-02T03:04:05+09:00", body: str = BODY) -> str:
    return (
        "---\n"
        + FRONT_MATTER_BEFORE_DATE
        + f"Date: {date}\n"
        + "Draft: true\n"
        + FRONT_MATTER_AFTER_DRAFT
        + "---\n"
        + body
    )


def published_text(date: str, body: str = BODY) -> str:
    return "---\n" + FRONT_MATTER_BEFORE_DATE + f"Date: {date}\n" + FRONT_MATTER_AFTER_DRAFT + "---\n" + body


class PreparePublishTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.entry_dir = Path(self._tmp.name) / "kiririmode.hatenablog.jp" / "entry"
        self.draft_dir = self.entry_dir / "_draft"
        self.draft_dir.mkdir(parents=True)
        self.draft = self.draft_dir / f"{ENTRY_ID}.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("HATENA_")}
        return subprocess.run(
            [sys.executable, str(CLI), str(self.draft), *args],
            capture_output=True,
            text=True,
            env=env,
            cwd=self._tmp.name,
        )

    def published_entries(self) -> list[Path]:
        return sorted(self.entry_dir.glob("[0-9]*/*.md"))

    def test_publishes_draft_with_current_date_and_without_draft_flag(self) -> None:
        self.draft.write_text(draft_text(), encoding="utf-8")
        before = datetime.now(JST).replace(microsecond=0)

        result = self.run_cli()

        after = datetime.now(JST)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.draft.exists())
        [entry] = self.published_entries()
        self.assertEqual(entry.name, f"{ENTRY_ID}.md")
        text = entry.read_text(encoding="utf-8")

        date_match = re.search(r"^Date: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+09:00)$", text, re.MULTILINE)
        self.assertIsNotNone(date_match, text)
        published_at = datetime.fromisoformat(date_match.group(1))
        self.assertTrue(before <= published_at <= after, published_at)
        self.assertEqual(entry.parent.name, published_at.strftime("%Y%m%d"))
        self.assertEqual(text, published_text(date_match.group(1)))

    def test_keep_date_leaves_date_and_uses_it_for_published_dir(self) -> None:
        self.draft.write_text(draft_text(date="2020-01-02T03:04:05+09:00"), encoding="utf-8")

        result = self.run_cli("--keep-date")

        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.entry_dir / "20200102" / f"{ENTRY_ID}.md"
        self.assertEqual(self.published_entries(), [entry])
        self.assertEqual(entry.read_text(encoding="utf-8"), published_text("2020-01-02T03:04:05+09:00"))
        self.assertFalse(self.draft.exists())

    def test_moves_own_attached_files_and_leaves_other_entries_files(self) -> None:
        self.draft.write_text(draft_text(), encoding="utf-8")
        (self.draft_dir / f"{ENTRY_ID}-architecture.svg").write_text("<svg/>", encoding="utf-8")
        (self.draft_dir / f"{ENTRY_ID}-architecture.png").write_bytes(b"\x89PNG own")
        other_draft = self.draft_dir / "9999999999.md"
        other_draft.write_text(draft_text(), encoding="utf-8")
        other_file = self.draft_dir / "9999999999-architecture.png"
        other_file.write_bytes(b"\x89PNG other")
        prefix_lookalike = self.draft_dir / f"{ENTRY_ID}0-note.png"
        prefix_lookalike.write_bytes(b"\x89PNG lookalike")

        result = self.run_cli("--keep-date")

        self.assertEqual(result.returncode, 0, result.stderr)
        published_dir = self.entry_dir / "20200102"
        self.assertEqual(
            sorted(p.name for p in published_dir.iterdir()),
            [f"{ENTRY_ID}-architecture.png", f"{ENTRY_ID}-architecture.svg", f"{ENTRY_ID}.md"],
        )
        self.assertEqual((published_dir / f"{ENTRY_ID}-architecture.png").read_bytes(), b"\x89PNG own")
        self.assertEqual(
            sorted(p.name for p in self.draft_dir.iterdir()),
            [prefix_lookalike.name, other_file.name, other_draft.name],
        )

    def test_stops_and_keeps_draft_when_local_image_reference_remains(self) -> None:
        original = draft_text(body=BODY + f"\n![構成図](./{ENTRY_ID}-architecture.svg)\n")
        self.draft.write_text(original, encoding="utf-8")
        attached = self.draft_dir / f"{ENTRY_ID}-architecture.svg"
        attached.write_text("<svg/>", encoding="utf-8")

        result = self.run_cli()

        self.assertEqual(result.returncode, 1)
        self.assertIn("upload-images", result.stderr)
        self.assertIn(f"./{ENTRY_ID}-architecture.svg", result.stderr)
        self.assertEqual(self.draft.read_text(encoding="utf-8"), original)
        self.assertTrue(attached.exists())
        self.assertEqual([p.name for p in self.entry_dir.iterdir()], ["_draft"])


if __name__ == "__main__":
    unittest.main()
