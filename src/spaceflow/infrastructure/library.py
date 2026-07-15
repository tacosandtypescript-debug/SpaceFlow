from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from spaceflow.domain.models import AudioAsset, Space, SpaceId


def safe_name(value: str, limit: int = 96) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^A-Za-z0-9._ -]+", "", ascii_value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ._-")
    return (cleaned or "space")[:limit].rstrip(" .")


class JsonLibraryRepository:
    def __init__(self, root: Path) -> None:
        self._root = root.expanduser()

    @property
    def root(self) -> Path:
        self._root.mkdir(parents=True, exist_ok=True)
        return self._root

    def destination_stem(self, space: Space) -> Path:
        return self.root / f"{safe_name(space.title)} [{space.id.value}]"

    def save_metadata(self, space: Space, audio_path: Path, audio_format: str) -> AudioAsset:
        metadata_path = audio_path.with_suffix(audio_path.suffix + ".json")
        asset = AudioAsset(space.id, audio_path, metadata_path, audio_format)
        data = {
            "schema_version": 1,
            "space": space.to_dict(),
            "asset": asset.to_dict(),
        }
        temporary = metadata_path.with_suffix(metadata_path.suffix + ".tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(metadata_path)
        return asset

    def list_assets(self) -> list[AudioAsset]:
        assets: list[AudioAsset] = []
        for metadata in self.root.glob("*.json"):
            try:
                data = json.loads(metadata.read_text(encoding="utf-8"))
                item = data["asset"]
                path = Path(item["path"])
                if not path.is_file():
                    continue
                created = datetime.fromisoformat(item["created_at"])
                assets.append(
                    AudioAsset(
                        SpaceId(item["space_id"]), path, metadata, item["format"], created
                    )
                )
            except (OSError, KeyError, ValueError, json.JSONDecodeError):
                continue
        return sorted(assets, key=lambda item: item.created_at, reverse=True)

    def delete(self, query: str) -> int:
        removed = 0
        for asset in self.list_assets():
            if query not in {asset.space_id.value, asset.path.name, str(asset.path)}:
                continue
            for path in (asset.path, asset.metadata_path):
                try:
                    path.unlink()
                    removed += 1
                except FileNotFoundError:
                    pass
            break
        return removed
