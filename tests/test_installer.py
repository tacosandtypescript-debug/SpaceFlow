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

    def test_ashell_profile_is_stored_in_documents(self):
        script = (ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        path_block = script.split('case ":${PATH}:" in', 1)[1]
        path_block = path_block.split('echo "SpaceFlow instalado', 1)[0]
        self.assertIn('if [ "$PLATFORM" = "ashell" ]', path_block)
        self.assertIn('PROFILE="$HOME/Documents/.profile"', path_block)
        self.assertIn('PROFILE="$HOME/.profile"', path_block)
        self.assertIn('grep -F "$PATH_LINE" "$PROFILE"', path_block)


if __name__ == "__main__":
    unittest.main()
