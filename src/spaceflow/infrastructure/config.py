from __future__ import annotations

import json
import os
import platform
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def detect_platform() -> str:
    prefix = os.environ.get("PREFIX", "").lower()
    appname = os.environ.get("APPNAME", "").lower()
    if "com.termux" in prefix or os.environ.get("TERMUX_VERSION"):
        return "termux"
    if "a-shell" in appname or platform.system() in {"iOS", "Darwin"} and Path.home().joinpath("Documents").exists():
        return "ashell"
    if os.name == "nt":
        return "windows"
    return "unix"


def default_data_dir() -> Path:
    kind = detect_platform()
    if kind == "windows":
        return Path(os.environ.get("APPDATA", Path.home())) / "SpaceFlow"
    if kind == "ashell":
        return Path.home() / "Documents" / ".spaceflow"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "spaceflow"


def default_library_dir() -> Path:
    kind = detect_platform()
    if kind == "windows":
        return Path.home() / "Music" / "SpaceFlow"
    if kind == "ashell":
        return Path.home() / "Documents" / "SpaceFlow"
    if kind == "termux" and (Path.home() / "storage" / "music").exists():
        return Path.home() / "storage" / "music" / "SpaceFlow"
    return Path.home() / "SpaceFlow"


@dataclass(slots=True)
class AppConfig:
    library_dir: str
    cookies_file: str
    default_format: str = "m4a"
    update_repo: str = "tacosandtypescript-debug/SpaceFlow"
    last_update_check: str | None = None


class ConfigStore:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = (data_dir or default_data_dir()).expanduser()
        self.path = self.data_dir / "config.json"

    def load(self) -> AppConfig:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        defaults = AppConfig(
            library_dir=str(default_library_dir()),
            cookies_file=str(self.data_dir / "cookies.txt"),
        )
        if not self.path.exists():
            self.save(defaults)
            return defaults
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return defaults
        valid = {key: raw[key] for key in asdict(defaults) if key in raw}
        return AppConfig(**{**asdict(defaults), **valid})

    def save(self, config: AppConfig) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(asdict(config), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)

    def set_value(self, key: str, value: str) -> AppConfig:
        config = self.load()
        if key not in {"library_dir", "default_format"}:
            raise ValueError("Solo se pueden modificar library_dir y default_format")
        if key == "default_format" and value not in {"m4a", "mp3"}:
            raise ValueError("El formato debe ser m4a o mp3")
        setattr(config, key, value)
        self.save(config)
        return config

    def public_dict(self) -> dict[str, Any]:
        config = self.load()
        return {
            "library_dir": config.library_dir,
            "cookies_file": config.cookies_file,
            "cookies_present": Path(config.cookies_file).is_file(),
            "default_format": config.default_format,
            "update_repo": config.update_repo,
            "last_update_check": config.last_update_check,
            "platform": detect_platform(),
        }

    def get_last_update_check(self) -> datetime | None:
        value = self.load().last_update_check
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def set_last_update_check(self, value: datetime) -> None:
        config = self.load()
        config.last_update_check = value.isoformat()
        self.save(config)
