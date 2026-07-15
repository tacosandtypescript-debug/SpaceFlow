from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_termux_launcher_uses_prefix_bin(self):
        script = (ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        termux_branch = script.split('elif [ -n "${TERMUX_VERSION:-}" ]', 1)[1]
        termux_branch = termux_branch.split("elif {", 1)[0]
        self.assertIn('BIN_DIR="$PREFIX/bin"', termux_branch)
        self.assertNotIn('BIN_DIR="$HOME/.local/bin"', termux_branch)


if __name__ == "__main__":
    unittest.main()
