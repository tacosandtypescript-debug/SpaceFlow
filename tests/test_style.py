from __future__ import annotations

import io
import os
import unittest
from unittest.mock import patch

from spaceflow.presentation.style import BOLD, CYAN, colors_enabled, paint


class Terminal(io.StringIO):
    def __init__(self, tty: bool) -> None:
        super().__init__()
        self.tty = tty

    def isatty(self) -> bool:
        return self.tty


class StyleTests(unittest.TestCase):
    def test_color_is_used_on_interactive_terminals(self):
        with patch.dict(os.environ, {}, clear=True):
            result = paint("SpaceFlow", BOLD, CYAN, stream=Terminal(True))
        self.assertEqual(result, "\033[1;36mSpaceFlow\033[0m")

    def test_no_color_is_respected(self):
        with patch.dict(os.environ, {"NO_COLOR": "1"}, clear=True):
            self.assertFalse(colors_enabled(Terminal(True)))
            self.assertEqual(paint("SpaceFlow", CYAN, stream=Terminal(True)), "SpaceFlow")

    def test_color_is_disabled_when_output_is_redirected(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(colors_enabled(Terminal(False)))


if __name__ == "__main__":
    unittest.main()
