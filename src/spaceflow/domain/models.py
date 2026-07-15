from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class SpaceState(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    UNKNOWN = "unknown"


class ParticipantRole(str, Enum):
    HOST = "host"
    COHOST = "cohost"
    SPEAKER = "speaker"


@dataclass(frozen=True)
class SpaceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or len(self.value) > 32 or not self.value.isalnum():
            raise ValueError("Identificador de Space inválido")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Participant:
    id: str
    name: str
    username: str | None = None
    role: ParticipantRole = ParticipantRole.SPEAKER

    @property
    def display_name(self) -> str:
        return f"{self.name} (@{self.username})" if self.username else self.name


@dataclass
class Space:
    id: SpaceId
    source_url: str
    space_url: str
    title: str
    state: SpaceState = SpaceState.UNKNOWN
    host: Participant | None = None
    participants: list[Participant] = field(default_factory=list)
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_seconds: int | None = None
    participant_count: int | None = None
    view_count: int | None = None
    description: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["id"] = self.id.value
        data["state"] = self.state.value
        for key in ("started_at", "ended_at"):
            value = getattr(self, key)
            data[key] = value.isoformat() if value else None
        data.pop("raw", None)
        return data


@dataclass(frozen=True)
class AudioAsset:
    space_id: SpaceId
    path: Path
    metadata_path: Path
    format: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "space_id": self.space_id.value,
            "path": str(self.path),
            "metadata_path": str(self.metadata_path),
            "format": self.format,
            "created_at": self.created_at.isoformat(),
        }
