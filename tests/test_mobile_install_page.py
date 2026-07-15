from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MobileInstallPageTests(unittest.TestCase):
    def test_readme_links_separate_apple_and_android_copy_pages(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("?device=apple", readme)
        self.assertIn("?device=android", readme)
        self.assertIn("COPIAR_PARA_TERMUX", readme)
        self.assertIn("COPIAR_PARA_a--SHELL_O_iSH", readme)

    def test_mobile_page_has_one_touch_copy_for_both_platforms(self):
        page = (ROOT / "site" / "index.html").read_text(encoding="utf-8")

        self.assertIn('data-device="apple"', page)
        self.assertIn('data-device="android"', page)
        self.assertIn("navigator.clipboard.writeText", page)
        self.assertIn("document.execCommand('copy')", page)
        self.assertIn("spaceflow</code>, no <code>flow", page)


if __name__ == "__main__":
    unittest.main()
