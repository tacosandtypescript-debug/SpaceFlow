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

    def stream_url(self, url: str) -> str:
        return "https://media.example/space.m3u8"

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
        self.played_url = None

    def play(self, path: Path) -> None:
        self.played = path

    def play_url(self, url: str) -> None:
        self.played_url = url


class ServiceTests(unittest.TestCase):
    def test_stream_playback_does_not_download_the_space(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            player = Player()
            service = SpaceFlowService(Resolver(), Media(root), Library(root), player)
            stream_url = service.play_url("https://x.com/user/status/123")
            self.assertEqual(stream_url, "https://media.example/space.m3u8")
            self.assertEqual(player.played_url, stream_url)
            self.assertIsNone(player.played)

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
