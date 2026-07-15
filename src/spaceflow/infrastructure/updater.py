from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from spaceflow.application.ports import ReleaseInfo
from spaceflow.domain.errors import UpdateFailed


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.match(r"^v?(\d+(?:\.\d+)*)", value.strip())
    return tuple(int(part) for part in match.group(1).split(".")) if match else (0,)


class GitHubReleaseRepository:
    def __init__(self, repository: str, current_version: str) -> None:
        self.repository = repository
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repository}/releases/latest"

    def latest(self) -> ReleaseInfo | None:
        request = urllib.request.Request(
            self.api_url,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "SpaceFlow-Updater"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.load(response)
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            return None
        version = str(payload.get("tag_name") or "").lstrip("v")
        if version_tuple(version) <= version_tuple(self.current_version):
            return None
        assets = {item.get("name"): item.get("browser_download_url") for item in payload.get("assets", [])}
        asset_url = assets.get("spaceflow.pyz")
        checksum_url = assets.get("SHA256SUMS")
        if not asset_url or not checksum_url:
            return None
        return ReleaseInfo(version, asset_url, checksum_url, str(payload.get("html_url") or ""))

    def install(self, release: ReleaseInfo) -> None:
        target = Path(sys.argv[0]).resolve()
        if target.suffix != ".pyz" or not target.is_file():
            raise UpdateFailed(
                "La actualización automática requiere la instalación spaceflow.pyz. Usa pip para actualizar este entorno."
            )
        with tempfile.TemporaryDirectory(prefix="spaceflow-update-") as directory:
            downloaded = Path(directory) / "spaceflow.pyz"
            checksums = Path(directory) / "SHA256SUMS"
            self._download(release.asset_url, downloaded)
            self._download(release.checksum_url, checksums)
            expected = self._expected_hash(checksums.read_text(encoding="utf-8"))
            actual = hashlib.sha256(downloaded.read_bytes()).hexdigest()
            if actual.lower() != expected.lower():
                raise UpdateFailed("El checksum de la actualización no coincide; no se instaló nada.")
            backup = target.with_suffix(target.suffix + ".old")
            try:
                if backup.exists():
                    backup.unlink()
                shutil.copy2(target, backup)
                os.replace(downloaded, target)
            except OSError as exc:
                if backup.exists() and not target.exists():
                    os.replace(backup, target)
                raise UpdateFailed(f"No se pudo reemplazar SpaceFlow: {exc}") from exc

    @staticmethod
    def _download(url: str, destination: Path) -> None:
        request = urllib.request.Request(url, headers={"User-Agent": "SpaceFlow-Updater"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
                shutil.copyfileobj(response, output)
        except (OSError, urllib.error.URLError) as exc:
            raise UpdateFailed(f"No se pudo descargar la actualización: {exc}") from exc

    @staticmethod
    def _expected_hash(text: str) -> str:
        for line in text.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-1].lstrip("*") == "spaceflow.pyz":
                return parts[0]
        raise UpdateFailed("SHA256SUMS no contiene spaceflow.pyz")
