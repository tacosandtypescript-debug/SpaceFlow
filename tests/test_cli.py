from __future__ import annotations

import unittest
from types import SimpleNamespace

from spaceflow.presentation.cli import _notice_update, parser


class CliTests(unittest.TestCase):
    def test_download_arguments(self):
        args = parser().parse_args(["download", "https://x.com/i/spaces/AbC123", "--format", "mp3"])
        self.assertEqual(args.command, "download")
        self.assertEqual(args.format, "mp3")

    def test_record_now_disables_from_start(self):
        args = parser().parse_args(["record", "https://x.com/i/spaces/AbC123", "--now"])
        self.assertFalse(args.from_start)

    def test_startup_forces_an_update_check(self):
        class Updates:
            def check(self, force=False):
                self.force = force
                return None

        updates = Updates()
        _notice_update(SimpleNamespace(updates=updates))
        self.assertTrue(updates.force)


if __name__ == "__main__":
    unittest.main()
