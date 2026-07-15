from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from spaceflow.domain.errors import PlaybackFailed
from spaceflow.infrastructure.config import detect_platform


class SystemAudioPlayer:
    def play(self, path: Path) -> None:
        path = path.expanduser().resolve()
        if not path.is_file():
            raise PlaybackFailed(f"No existe el audio: {path}")
        kind = detect_platform()
        try:
            if kind == "windows":
                os.startfile(str(path))  # type: ignore[attr-defined]
                return
            if kind == "termux":
                command = shutil.which("termux-media-player") or shutil.which("termux-open")
                if command:
                    args = [command, "play", str(path)] if command.endswith("termux-media-player") else [command, str(path)]
                    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
            command = shutil.which("open") or shutil.which("xdg-open")
            if command:
                subprocess.Popen([command, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        except OSError as exc:
            raise PlaybackFailed(f"No se pudo abrir el reproductor: {exc}") from exc
        raise PlaybackFailed(
            f"No encontré un reproductor automático. Abre manualmente: {path}"
        )
