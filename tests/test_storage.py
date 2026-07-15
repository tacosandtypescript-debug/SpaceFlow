from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from spaceflow.domain.errors import AuthenticationRequired, SpaceFlowError
from spaceflow.domain.models import Space, SpaceId
from spaceflow.infrastructure.config import ConfigStore
from spaceflow.infrastructure.cookies import NetscapeCookieStore
from spaceflow.infrastructure.library import JsonLibraryRepository, safe_name


COOKIE = "# Netscape HTTP Cookie File\n.x.com\tTRUE\t/\tTRUE\t2147483647\tauth_token\tsecret\n"


class StorageTests(unittest.TestCase):
    def test_cookie_import_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_text(COOKIE, encoding="utf-8")
            store = NetscapeCookieStore(root / "private" / "cookies.txt")
            imported = store.import_file(source)
            self.assertEqual(imported, store.require())
            self.assertIn("auth_token", imported.read_text(encoding="utf-8"))
            if os.name != "nt":
                self.assertEqual(imported.stat().st_mode & 0o777, 0o600)

    def test_missing_and_invalid_cookies_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NetscapeCookieStore(Path(directory) / "cookies.txt")
            with self.assertRaises(AuthenticationRequired):
                store.require()
            invalid = Path(directory) / "bad.txt"
            invalid.write_text("not cookies", encoding="utf-8")
            with self.assertRaises(SpaceFlowError):
                store.import_file(invalid)

    def test_config_has_no_cookie_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ConfigStore(Path(directory))
            config = store.load()
            raw = json.loads(store.path.read_text(encoding="utf-8"))
            self.assertEqual(raw["cookies_file"], config.cookies_file)
            self.assertNotIn("auth_token", store.path.read_text(encoding="utf-8"))

    def test_library_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            library = JsonLibraryRepository(Path(directory))
            space = Space(SpaceId("AbC123"), "source", "space", "Título / extraño")
            audio = library.destination_stem(space).with_suffix(".m4a")
            audio.write_bytes(b"audio")
            asset = library.save_metadata(space, audio, "m4a")
            listed = library.list_assets()
            self.assertEqual([item.space_id.value for item in listed], ["AbC123"])
            self.assertEqual(library.delete(asset.space_id.value), 2)
            self.assertFalse(audio.exists())

    def test_safe_name_blocks_paths(self):
        self.assertNotIn("/", safe_name("../../bad/name"))
        self.assertNotIn("\\", safe_name("..\\bad"))


if __name__ == "__main__":
    unittest.main()
