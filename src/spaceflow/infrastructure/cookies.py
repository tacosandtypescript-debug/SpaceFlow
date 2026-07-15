from __future__ import annotations

import os
import shutil
from pathlib import Path

from spaceflow.domain.errors import AuthenticationRequired, SpaceFlowError


class NetscapeCookieStore:
    def __init__(self, destination: Path) -> None:
        self._path = destination.expanduser()

    @property
    def path(self) -> Path:
        return self._path

    def import_file(self, source: Path) -> Path:
        source = source.expanduser().resolve()
        if not source.is_file():
            raise SpaceFlowError(f"No existe el archivo: {source}")
        self._validate(source)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(".tmp")
        shutil.copyfile(source, temporary)
        try:
            os.chmod(temporary, 0o600)
        except OSError:
            pass
        os.replace(temporary, self._path)
        return self._path

    def require(self) -> Path:
        if not self._path.is_file():
            raise AuthenticationRequired(
                "Faltan las cookies de X. Usa: spaceflow auth import /ruta/cookies.txt"
            )
        self._validate(self._path)
        return self._path

    @staticmethod
    def _validate(path: Path) -> None:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            raise SpaceFlowError(f"No se pudieron leer las cookies: {exc}") from exc
        cookie_lines = [line for line in lines if line and not line.startswith("#")]
        if not cookie_lines or not any(len(line.split("\t")) >= 7 for line in cookie_lines):
            raise SpaceFlowError("El archivo no parece estar en formato Netscape cookies.txt")
