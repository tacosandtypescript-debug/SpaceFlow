from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spaceflow.infrastructure.yt_dlp_provider import YtDlpSpaceProvider


class OptionalCookiesTests(unittest.TestCase):
    def test_missing_cookie_file_is_not_sent_to_yt_dlp(self):
        with tempfile.TemporaryDirectory() as directory:
            provider = YtDlpSpaceProvider(Path(directory) / "cookies.txt")
            self.assertEqual(provider._cookie_options(), {})

    def test_imported_cookie_file_is_sent_to_yt_dlp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cookies.txt"
            path.write_text("# Netscape HTTP Cookie File\n", encoding="utf-8")
            provider = YtDlpSpaceProvider(path)
            self.assertEqual(provider._cookie_options(), {"cookiefile": str(path)})


if __name__ == "__main__":
    unittest.main()
