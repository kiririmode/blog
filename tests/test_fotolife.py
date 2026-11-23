"""フォトライフへのアップロードを、返す URL で確かめる。

フォトライフの API は外部システムなので、HTTP の送受信（urllib.request.urlopen）だけを偽物に替える。
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fotolife  # noqa: E402

RETURNED_URL = "https://cdn-ak.f.st-hatena.com/images/fotolife/k/kiririmode/20261123/20261123120510.png"
RESPONSE = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#" xmlns:hatena="http://www.hatena.ne.jp/info/xmlns#">
  <title>figure</title>
  <hatena:imageurl>{RETURNED_URL}</hatena:imageurl>
</entry>
""".encode()


class UploadPngTest(unittest.TestCase):
    def test_returns_the_url_fotolife_returns_as_is(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "figure.png"
            png.write_bytes(b"\x89PNG")
            env = {"HATENA_USERNAME": "user", "HATENA_API_KEY": "key"}
            with mock.patch.dict(os.environ, env), mock.patch(
                "urllib.request.urlopen", return_value=io.BytesIO(RESPONSE)
            ):
                url = fotolife.upload_png(png, "figure")

        self.assertEqual(url, RETURNED_URL)


if __name__ == "__main__":
    unittest.main()
