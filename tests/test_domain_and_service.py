from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spaceflow.application.services import SpaceFlowService
from spaceflow.domain.models import AudioAsset, Space, SpaceId, SpaceState


class Resolver:
    def resolve(self, url: str) -> str:
        return "https://x.com/i/spaces/AbC123"


class Media:
    def __init__(self, root: Path) -> None:
        self.root = root

    def get_info(self, url: str) -> Space:
        return Space(SpaceId("AbC123"), url, url, "Un Space", SpaceState.ENDED)

    def download(self, space, destination_stem, audio_format, live_from_start=True):
        path = destination_stem.with_suffix("." + audio_format)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"audio")
        return path, False


class Library:
    def __init__(self, root: Path) -> None:
        self.root = root

    def destination_stem(self, space: Space) -> Path:
        return self.root / f"{space.title} [{space.id.value}]"

    def save_metadata(self, space, audio_path, audio_format):
        metadata = audio_path.with_suffix(audio_path.suffix + ".json")
        metadata.write_text("{}", encoding="utf-8")
        return AudioAsset(space.id, audio_path, metadata, audio_format)


class Player:
    def __init__(self) -> None:
        self.played = None

    def play(self, path: Path) -> None:
        self.played = path


class ServiceTests(unittest.TestCase):
    def test_download_and_play_are_orchestrated_without_infrastructure_details(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            player = Player()
            service = SpaceFlowService(Resolver(), Media(root), Library(root), player)
            asset = service.play_url("https://x.com/user/status/123")
            self.assertEqual(asset.space_id.value, "AbC123")
            self.assertEqual(player.played, asset.path)
            self.assertTrue(asset.path.is_file())

    def test_space_serialization_excludes_raw_provider_payload(self):
        space = Space(
            SpaceId("AbC123"), "source", "space", "Title", SpaceState.LIVE, raw={"secret": "x"}
        )
        data = space.to_dict()
        self.assertEqual(data["id"], "AbC123")
        self.assertEqual(data["state"], "live")
        self.assertNotIn("raw", data)


if __name__ == "__main__":
    unittest.main()
