from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Protocol

from spaceflow.domain.models import AudioAsset, Space


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    version: str
    asset_url: str
    checksum_url: str
    page_url: str


class SpaceUrlResolver(Protocol):
    def resolve(self, url: str) -> str: ...


class SpaceMediaProvider(Protocol):
    def get_info(self, url: str) -> Space: ...

    def download(
        self,
        space: Space,
        destination_stem: Path,
        audio_format: str,
        live_from_start: bool = True,
    ) -> tuple[Path, bool]: ...


class LibraryRepository(Protocol):
    @property
    def root(self) -> Path: ...

    def destination_stem(self, space: Space) -> Path: ...

    def save_metadata(self, space: Space, audio_path: Path, audio_format: str) -> AudioAsset: ...

    def list_assets(self) -> list[AudioAsset]: ...

    def delete(self, query: str) -> int: ...


class AudioPlayer(Protocol):
    def play(self, path: Path) -> None: ...


class CookieStore(Protocol):
    @property
    def path(self) -> Path: ...

    def import_file(self, source: Path) -> Path: ...

    def require(self) -> Path: ...


class UpdateRepository(Protocol):
    def latest(self) -> ReleaseInfo | None: ...

    def install(self, release: ReleaseInfo) -> None: ...


class UpdateStateStore(Protocol):
    def get_last_update_check(self) -> datetime | None: ...

    def set_last_update_check(self, value: datetime) -> None: ...
