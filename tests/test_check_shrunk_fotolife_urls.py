"""縮小版 URL の検査 CLI を、外から見える振る舞い（終了コードと報告）で確かめる。"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parent.parent / "scripts" / "check_shrunk_fotolife_urls.py"

SHRUNK_URL = "https://cdn-ak.f.st-hatena.com/images/fotolife/k/kiririmode/20261123/20261123112530.png"
ORIGINAL_URL = "https://cdn-ak.f.st-hatena.com/images/fotolife/k/kiririmode/20261123/20261123112530_original.png"


def run_check(*files: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *map(str, files)],
        capture_output=True,
        text=True,
    )


class CheckShrunkFotolifeUrlsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_reports_shrunk_url_with_file_and_line_and_fails(self) -> None:
        entry = self.write("123.md", f"# title\n\nbody\n![構成図]({SHRUNK_URL})\n")

        result = run_check(entry)

        self.assertEqual(result.returncode, 1)
        self.assertIn(f"{entry}:4:", result.stderr)
        self.assertIn(SHRUNK_URL, result.stderr)

    def test_passes_entry_with_only_original_urls(self) -> None:
        entry = self.write("123.md", f"![構成図]({ORIGINAL_URL})\n[link](https://example.com/a.png)\n")

        result = run_check(entry)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    def test_reports_only_the_violating_file_among_many(self) -> None:
        clean = self.write("clean.md", f"![a]({ORIGINAL_URL})\n")
        dirty = self.write("dirty.md", f"text\n![a]({ORIGINAL_URL}) and ![b]({SHRUNK_URL})\n")

        result = run_check(clean, dirty)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.count(SHRUNK_URL), 1)
        self.assertIn(f"{dirty}:2:", result.stderr)
        self.assertNotIn(str(clean), result.stderr)


if __name__ == "__main__":
    unittest.main()
