from __future__ import annotations

import unittest
from unittest.mock import patch

from spaceflow.infrastructure.player import SystemAudioPlayer


class PlayerTests(unittest.TestCase):
    def test_termux_uses_mpv_for_hls_audio(self):
        player = SystemAudioPlayer()
        with patch(
            "spaceflow.infrastructure.player.detect_platform", return_value="termux"
        ), patch(
            "spaceflow.infrastructure.player.shutil.which", return_value="/bin/mpv"
        ), patch("spaceflow.infrastructure.player.subprocess.run") as run:
            player.play_url("https://media.example/space.m3u8")
        run.assert_called_once_with(
            ["/bin/mpv", "--no-video", "--really-quiet", "https://media.example/space.m3u8"],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
