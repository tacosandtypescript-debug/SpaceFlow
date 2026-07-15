from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spaceflow import __version__
from spaceflow.application.services import SpaceFlowService
from spaceflow.application.update_service import UpdateService
from spaceflow.infrastructure.config import AppConfig, ConfigStore
from spaceflow.infrastructure.cookies import NetscapeCookieStore
from spaceflow.infrastructure.library import JsonLibraryRepository
from spaceflow.infrastructure.player import SystemAudioPlayer
from spaceflow.infrastructure.resolver import XSpaceUrlResolver
from spaceflow.infrastructure.updater import GitHubReleaseRepository
from spaceflow.infrastructure.yt_dlp_provider import YtDlpSpaceProvider


@dataclass
class Container:
    config_store: ConfigStore
    config: AppConfig
    cookies: NetscapeCookieStore
    library: JsonLibraryRepository
    service: SpaceFlowService
    updates: UpdateService


def build_container(data_dir: Path | None = None) -> Container:
    config_store = ConfigStore(data_dir)
    config = config_store.load()
    cookies = NetscapeCookieStore(Path(config.cookies_file))
    library = JsonLibraryRepository(Path(config.library_dir))
    resolver = XSpaceUrlResolver(cookies.path)
    media = YtDlpSpaceProvider(cookies.path)
    player = SystemAudioPlayer()
    service = SpaceFlowService(resolver, media, library, player, cookies)
    releases = GitHubReleaseRepository(config.update_repo, __version__)
    updates = UpdateService(releases, config_store)
    return Container(config_store, config, cookies, library, service, updates)
