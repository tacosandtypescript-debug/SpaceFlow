from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from spaceflow.infrastructure.yt_dlp_provider import YtDlpSpaceProvider


class FakeYoutubeDL:
    seen_options = []

    def __init__(self, options):
        self.options = options
        self.seen_options.append(options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def extract_info(self, url, download=False):
        return {
            "id": "AbC123",
            "title": "Space público",
            "webpage_url": url,
            "url": "https://media.example/space.m3u8",
        }

    def download(self, urls):
        return 0


class FakeYtDlp:
    YoutubeDL = FakeYoutubeDL


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

    def test_python_deprecation_warnings_are_suppressed(self):
        FakeYoutubeDL.seen_options.clear()
        provider = YtDlpSpaceProvider(Path("missing-cookies.txt"))
        with patch(
            "spaceflow.infrastructure.yt_dlp_provider._load_yt_dlp",
            return_value=FakeYtDlp,
        ):
            provider.get_info("https://x.com/i/spaces/AbC123")
            provider._run_download(
                "https://x.com/i/spaces/AbC123", Path("audio"), "m4a", False
            )
        self.assertEqual(len(FakeYoutubeDL.seen_options), 2)
        self.assertTrue(all(item["no_warnings"] for item in FakeYoutubeDL.seen_options))

    def test_stream_url_returns_the_resolved_hls_url(self):
        provider = YtDlpSpaceProvider(Path("missing-cookies.txt"))
        with patch(
            "spaceflow.infrastructure.yt_dlp_provider._load_yt_dlp",
            return_value=FakeYtDlp,
        ):
            result = provider.stream_url("https://x.com/i/spaces/AbC123")
        self.assertEqual(result, "https://media.example/space.m3u8")

    def test_user_cancellation_is_not_reported_as_broken_ffmpeg(self):
        provider = YtDlpSpaceProvider(Path("missing-cookies.txt"))
        result = provider._friendly_error(
            RuntimeError("ffmpeg exited with code 255 after received signal 2")
        )
        self.assertEqual(result, "Operación cancelada antes de terminar.")

    def test_speaker_names_are_recovered_from_twitter_space_metadata(self):
        info = {
            "description": "Twitter Space participated by Ana, Bruno",
        }
        participants = YtDlpSpaceProvider._participants(info, None)
        self.assertEqual([item.name for item in participants], ["Ana", "Bruno"])

    def test_nobody_yet_is_not_shown_as_a_speaker(self):
        info = {"description": "Twitter Space participated by nobody yet"}
        self.assertEqual(YtDlpSpaceProvider._participants(info, None), [])


if __name__ == "__main__":
    unittest.main()
