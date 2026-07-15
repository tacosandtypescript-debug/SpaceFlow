from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from spaceflow.domain.errors import DownloadFailed, SpaceUnavailable
from spaceflow.domain.models import Participant, ParticipantRole, Space, SpaceId, SpaceState
from spaceflow.infrastructure.library import safe_name


def _load_yt_dlp():
    try:
        import yt_dlp
    except ImportError as exc:
        raise SpaceUnavailable(
            "Falta yt-dlp. Ejecuta: python -m pip install --upgrade yt-dlp"
        ) from exc
    return yt_dlp


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, (int, float)):
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return None


class YtDlpSpaceProvider:
    def __init__(self, cookies_file: Path, quiet: bool = False) -> None:
        self.cookies_file = cookies_file
        self.quiet = quiet

    def get_info(self, url: str) -> Space:
        yt_dlp = _load_yt_dlp()
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
            **self._cookie_options(),
        }
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as exc:
            raise SpaceUnavailable(self._friendly_error(exc)) from exc
        if not isinstance(info, dict):
            raise SpaceUnavailable("X no devolvió información de este Space")
        return self._to_space(url, info)

    def download(
        self,
        space: Space,
        destination_stem: Path,
        audio_format: str,
        live_from_start: bool = True,
    ) -> tuple[Path, bool]:
        if audio_format not in {"m4a", "mp3"}:
            raise DownloadFailed("El formato debe ser m4a o mp3")
        destination_stem.parent.mkdir(parents=True, exist_ok=True)
        used_fallback = False
        try:
            self._run_download(space.space_url, destination_stem, audio_format, live_from_start)
        except Exception as first_error:
            if not live_from_start or space.state is not SpaceState.LIVE:
                raise DownloadFailed(self._friendly_error(first_error)) from first_error
            used_fallback = True
            try:
                self._run_download(space.space_url, destination_stem, audio_format, False)
            except Exception as second_error:
                raise DownloadFailed(self._friendly_error(second_error)) from second_error

        candidates = [
            path
            for path in destination_stem.parent.glob(destination_stem.name + ".*")
            if path.is_file()
            and not path.name.endswith((".json", ".part", ".ytdl", ".tmp"))
        ]
        preferred = [path for path in candidates if path.suffix.lower() == f".{audio_format}"]
        selected = max(preferred or candidates, key=lambda path: path.stat().st_mtime, default=None)
        if selected is None:
            raise DownloadFailed("La descarga terminó sin producir un archivo de audio")
        return selected, used_fallback

    def _run_download(
        self, url: str, stem: Path, audio_format: str, live_from_start: bool
    ) -> None:
        yt_dlp = _load_yt_dlp()
        options: dict[str, Any] = {
            "format": "bestaudio/best",
            "outtmpl": str(stem) + ".%(ext)s",
            "noplaylist": True,
            "continuedl": True,
            "retries": 10,
            "fragment_retries": 10,
            "concurrent_fragment_downloads": 1,
            "live_from_start": live_from_start,
            "no_warnings": True,
            **self._cookie_options(),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                    "preferredquality": "192" if audio_format == "mp3" else "0",
                }
            ],
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

    @staticmethod
    def _to_space(url: str, info: dict[str, Any]) -> Space:
        raw_id = str(info.get("id") or "")
        if not raw_id.isalnum() or len(raw_id) > 32:
            raw_id = url.rstrip("/").rsplit("/", 1)[-1].split("?", 1)[0]
        space_id = SpaceId(raw_id)
        live_status = str(info.get("live_status") or "").lower()
        state = {
            "is_live": SpaceState.LIVE,
            "is_upcoming": SpaceState.SCHEDULED,
            "post_live": SpaceState.ENDED,
            "was_live": SpaceState.ENDED,
            "not_live": SpaceState.ENDED,
        }.get(live_status, SpaceState.UNKNOWN)
        host_name = str(info.get("uploader") or info.get("channel") or "").strip()
        host_id = str(info.get("uploader_id") or info.get("channel_id") or host_name)
        host = None
        if host_name:
            host = Participant(
                id=host_id,
                name=host_name,
                username=str(info.get("uploader_id") or "") or None,
                role=ParticipantRole.HOST,
            )
        participants = YtDlpSpaceProvider._participants(info, host)
        duration = info.get("duration")
        return Space(
            id=space_id,
            source_url=str(info.get("original_url") or url),
            space_url=str(info.get("webpage_url") or url),
            title=str(info.get("title") or f"X Space {space_id.value}"),
            state=state,
            host=host,
            participants=participants,
            started_at=_timestamp(info.get("timestamp") or info.get("release_timestamp")),
            ended_at=None,
            duration_seconds=int(duration) if isinstance(duration, (int, float)) else None,
            participant_count=YtDlpSpaceProvider._integer(info.get("concurrent_view_count")),
            view_count=YtDlpSpaceProvider._integer(info.get("view_count")),
            description=str(info.get("description") or "") or None,
            raw={key: info.get(key) for key in ("extractor", "extractor_key", "live_status")},
        )

    @staticmethod
    def _participants(info: dict[str, Any], host: Participant | None) -> list[Participant]:
        result: list[Participant] = [host] if host else []
        seen = {host.id} if host else set()
        values = info.get("participants") or info.get("speakers") or []
        if not isinstance(values, list):
            return result
        for item in values:
            if not isinstance(item, dict):
                continue
            participant_id = str(item.get("id") or item.get("rest_id") or "")
            name = str(item.get("name") or item.get("display_name") or "").strip()
            if not participant_id or not name or participant_id in seen:
                continue
            role_name = str(item.get("role") or "speaker").lower()
            role = ParticipantRole.COHOST if "cohost" in role_name else ParticipantRole.SPEAKER
            result.append(
                Participant(participant_id, name, item.get("username") or item.get("screen_name"), role)
            )
            seen.add(participant_id)
        return result

    @staticmethod
    def _integer(value: Any) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def _cookie_options(self) -> dict[str, str]:
        if self.cookies_file.is_file():
            return {"cookiefile": str(self.cookies_file)}
        return {}

    def _friendly_error(self, error: Exception) -> str:
        message = str(error).replace("ERROR: ", "").strip()
        lowered = message.lower()
        if "cookies" in lowered or "login" in lowered or "unauthorized" in lowered:
            if self.cookies_file.is_file():
                return "X rechazó las cookies. Expórtalas otra vez e impórtalas con SpaceFlow."
            return (
                "Este Space requiere iniciar sesión en X. Importa cookies con: "
                "spaceflow auth import /ruta/cookies.txt"
            )
        if "ffmpeg" in lowered:
            return "FFmpeg no está instalado o no funciona. Ejecuta el instalador de SpaceFlow otra vez."
        if "not available" in lowered or "no longer available" in lowered:
            return "La grabación ya no está disponible en X."
        return message or "X no pudo entregar el Space"
