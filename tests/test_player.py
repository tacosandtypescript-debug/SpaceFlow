from __future__ import annotations

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from spaceflow.domain.errors import PlaybackFailed
from spaceflow.infrastructure.player import SystemAudioPlayer


class PlayerTests(unittest.TestCase):
    def test_termux_uses_mpv_for_hls_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            player = SystemAudioPlayer(Path(directory) / "mpv.sock")
            with patch(
                "spaceflow.infrastructure.player.detect_platform", return_value="termux"
            ), patch(
                "spaceflow.infrastructure.player.shutil.which", return_value="/bin/mpv"
            ), patch(
                "spaceflow.infrastructure.player.subprocess.Popen"
            ) as popen, patch.object(player, "_wait_for_mpv", return_value=True):
                player.play_url("https://media.example/space.m3u8")
            args = popen.call_args.args[0]
            self.assertIn("--input-ipc-server=" + str(player.mpv_socket), args)
            self.assertIn("--ao=opensles", args)
            self.assertIn("--volume=100", args)
            self.assertEqual(args[-1], "https://media.example/space.m3u8")
            self.assertTrue(popen.call_args.kwargs["start_new_session"])

    def test_termux_volume_uses_mpv_ipc(self):
        player = SystemAudioPlayer(Path("/tmp/spaceflow-test.sock"))
        with patch(
            "spaceflow.infrastructure.player.detect_platform", return_value="termux"
        ), patch.object(player, "_send_mpv_command") as send:
            player.change_volume(-10)
        send.assert_called_once_with(["add", "volume", -10])

    def test_stop_falls_back_to_saved_process_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            player = SystemAudioPlayer(root / "missing.sock", root / "mpv.pid")
            player.mpv_socket.touch()
            player.mpv_pid.write_text("1234", encoding="ascii")
            with patch(
                "spaceflow.infrastructure.player.detect_platform", return_value="termux"
            ), patch.object(
                player, "_send_mpv_command", side_effect=PlaybackFailed("sin IPC")
            ), patch("spaceflow.infrastructure.player.os.kill") as kill:
                player.stop()
            kill.assert_called_once_with(1234, __import__("signal").SIGTERM)
            self.assertFalse(player.mpv_pid.exists())


if __name__ == "__main__":
    unittest.main()
