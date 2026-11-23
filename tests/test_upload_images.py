"""ローカルの画像参照のアップロード CLI を、--dry-run の終了コードと出力で確かめる。

--dry-run はアップロードも本文の書き換えもしない。参照する画像は PNG にして、resvg なしで動かす。
誤ってアップロードしないよう、HATENA_ で始まる環境変数を外して CLI を走らせる。
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parent.parent / "scripts" / "upload_images.py"


class UploadImagesDryRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.markdown = self.dir / "123.md"
        (self.dir / "123-figure.png").write_bytes(b"\x89PNG")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self) -> subprocess.CompletedProcess[str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("HATENA_")}
        return subprocess.run(
            [sys.executable, str(CLI), str(self.markdown), "--dry-run"],
            capture_output=True,
            text=True,
            env=env,
        )

    def test_lists_local_image_reference_outside_code_block_only(self) -> None:
        text = "![図](./123-figure.png)\n\n```markdown\n![例](./example.png)\n```\n"
        self.markdown.write_text(text, encoding="utf-8")

        result = self.run_cli()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("![図](./123-figure.png)", result.stdout)
        self.assertNotIn("example.png", result.stdout)
        self.assertEqual(self.markdown.read_text(encoding="utf-8"), text)

    def test_rejects_extension_it_cannot_upload_before_processing_any(self) -> None:
        text = "![図](./123-figure.png)\n![写真](./photo.jpg)\n"
        self.markdown.write_text(text, encoding="utf-8")

        result = self.run_cli()

        self.assertEqual(result.returncode, 1)
        self.assertIn("./photo.jpg", result.stderr)
        self.assertNotIn("123-figure.png", result.stdout)


if __name__ == "__main__":
    unittest.main()
