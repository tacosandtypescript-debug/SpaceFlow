from __future__ import annotations

import json
import os
import signal
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path

from spaceflow.domain.errors import PlaybackFailed
from spaceflow.infrastructure.config import detect_platform


class SystemAudioPlayer:
    def __init__(self, mpv_socket: Path | None = None, mpv_pid: Path | None = None) -> None:
        self.mpv_socket = mpv_socket or Path(tempfile.gettempdir()) / "spaceflow-mpv.sock"
        self.mpv_pid = mpv_pid or Path(tempfile.gettempdir()) / "spaceflow-mpv.pid"

    def play_url(self, url: str) -> None:
        kind = detect_platform()
        try:
            if kind == "windows":
                os.startfile(url)  # type: ignore[attr-defined]
                return
            if kind == "termux":
                mpv = shutil.which("mpv")
                if mpv:
                    self._stop_existing_mpv()
                    try:
                        self.mpv_socket.unlink()
                    except FileNotFoundError:
                        pass
                    process = subprocess.Popen(
                        [
                            mpv,
                            "--no-video",
                            "--really-quiet",
                            "--ao=opensles",
                            "--volume=100",
                            f"--input-ipc-server={self.mpv_socket}",
                            url,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                    )
                    if not self._wait_for_mpv(process):
                        raise PlaybackFailed("MPV no pudo iniciar la reproducción.")
                    self.mpv_pid.write_text(str(process.pid), encoding="ascii")
                    return
                command = shutil.which("termux-open-url") or shutil.which("termux-open")
                if command:
                    subprocess.run([command, url], check=True)
                    return
            if kind == "ashell":
                subprocess.run(["open", url], check=True)
                return
            if kind == "ish":
                raise PlaybackFailed(
                    "iSH no ofrece salida de audio. Usa a-Shell para escuchar o descarga el archivo y ábrelo desde Archivos."
                )
            command = shutil.which("open") or shutil.which("xdg-open")
            if command:
                subprocess.run([command, url], check=True)
                return
        except PlaybackFailed:
            raise
        except (OSError, subprocess.SubprocessError) as exc:
            raise PlaybackFailed(f"No se pudo abrir el reproductor: {exc}") from exc
        raise PlaybackFailed("No encontré un reproductor para abrir el audio en streaming.")

    def pause(self) -> None:
        self._mpv_command(["set_property", "pause", True], signal.SIGSTOP)

    def resume(self) -> None:
        if detect_platform() != "termux":
            raise PlaybackFailed(
                "Los controles integrados están disponibles en Termux; usa los controles del sistema."
            )
        resumed = self._signal_mpv(signal.SIGCONT)
        try:
            self._send_mpv_command(["set_property", "pause", False])
            resumed = True
        except PlaybackFailed:
            if not resumed:
                raise

    def stop(self) -> None:
        if detect_platform() != "termux":
            raise PlaybackFailed(
                "Los controles integrados están disponibles en Termux; usa los controles del sistema."
            )
        stopped = False
        try:
            self._send_mpv_command(["quit"])
            stopped = True
        except PlaybackFailed:
            pass
        if self._signal_mpv(signal.SIGTERM):
            stopped = True
        if not stopped:
            raise PlaybackFailed(
                "No hay una reproducción activa. Elige primero Escuchar ahora."
            )
        self._remove_pid_file()

    def change_volume(self, delta: int) -> None:
        self._mpv_command(["add", "volume", int(delta)])

    def _stop_existing_mpv(self) -> None:
        try:
            self.stop()
            time.sleep(0.1)
        except PlaybackFailed:
            pass

    def _wait_for_mpv(self, process: subprocess.Popen) -> bool:
        for _ in range(20):
            if self.mpv_socket.exists():
                return True
            if process.poll() is not None:
                return False
            time.sleep(0.05)
        return self.mpv_socket.exists()

    def _mpv_command(self, command: list[object], fallback_signal: int | None = None) -> None:
        if detect_platform() != "termux":
            raise PlaybackFailed(
                "Los controles integrados están disponibles en Termux; usa los controles del sistema."
            )
        try:
            self._send_mpv_command(command)
        except PlaybackFailed:
            if fallback_signal is None or not self._signal_mpv(fallback_signal):
                raise

    def _signal_mpv(self, action: int) -> bool:
        try:
            pid = int(self.mpv_pid.read_text(encoding="ascii").strip())
            if not self.mpv_socket.exists():
                command_line = Path(f"/proc/{pid}/cmdline").read_bytes()
                if b"mpv" not in command_line.lower():
                    self._remove_pid_file()
                    return False
            os.kill(pid, action)
            return True
        except (OSError, ValueError):
            self._remove_pid_file()
            return False

    def _remove_pid_file(self) -> None:
        try:
            self.mpv_pid.unlink()
        except FileNotFoundError:
            pass

    def _send_mpv_command(self, command: list[object]) -> None:
        if not self.mpv_socket.exists():
            raise PlaybackFailed(
                "No hay una reproducción activa. Elige primero Escuchar ahora."
            )
        payload = (json.dumps({"command": command}) + "\n").encode("utf-8")
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                connection.settimeout(2)
                connection.connect(str(self.mpv_socket))
                connection.sendall(payload)
        except OSError as exc:
            raise PlaybackFailed(
                "No se pudo controlar el audio. Inicia de nuevo Escuchar ahora."
            ) from exc

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
