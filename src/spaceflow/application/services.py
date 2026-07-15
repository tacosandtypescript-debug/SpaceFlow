from __future__ import annotations

from pathlib import Path

from spaceflow.application.ports import (
    AudioPlayer,
    LibraryRepository,
    SpaceMediaProvider,
    SpaceUrlResolver,
)
from spaceflow.domain.models import AudioAsset, Space


class SpaceFlowService:
    def __init__(
        self,
        resolver: SpaceUrlResolver,
        media: SpaceMediaProvider,
        library: LibraryRepository,
        player: AudioPlayer,
    ) -> None:
        self.resolver = resolver
        self.media = media
        self.library = library
        self.player = player

    def info(self, url: str) -> Space:
        return self.media.get_info(self.resolver.resolve(url))

    def download(
        self,
        url: str,
        audio_format: str = "m4a",
        output_dir: Path | None = None,
        live_from_start: bool = True,
    ) -> tuple[AudioAsset, bool]:
        space = self.media.get_info(self.resolver.resolve(url))
        stem = self.library.destination_stem(space)
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            stem = output_dir / stem.name
        path, used_fallback = self.media.download(
            space, stem, audio_format, live_from_start=live_from_start
        )
        asset = self.library.save_metadata(space, path, audio_format)
        return asset, used_fallback

    def play_url(self, url: str, audio_format: str = "m4a") -> AudioAsset:
        asset, _ = self.download(url, audio_format=audio_format)
        self.player.play(asset.path)
        return asset

    def play_asset(self, asset: AudioAsset) -> None:
        self.player.play(asset.path)
