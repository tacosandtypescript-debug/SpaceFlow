from __future__ import annotations

from spaceflow.domain.models import Space


def _duration(seconds: int | None) -> str:
    if seconds is None:
        return "No disponible"
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:d}:{minutes:02d}:{secs:02d}"


def print_space(space: Space) -> None:
    print(f"\nTítulo: {space.title}")
    print(f"ID: {space.id.value}")
    print(f"Estado: {space.state.value}")
    print(f"Duración: {_duration(space.duration_seconds)}")
    print(f"Anfitrión: {space.host.display_name if space.host else 'No disponible'}")
    print(
        "Participantes conectados: "
        + (str(space.participant_count) if space.participant_count is not None else "No disponible")
    )
    print(
        "Reproducciones: "
        + (str(space.view_count) if space.view_count is not None else "No disponible")
    )
    speakers = [item for item in space.participants if not space.host or item.id != space.host.id]
    if speakers:
        print("Hablantes:")
        for speaker in speakers:
            print(f"  - {speaker.display_name} ({speaker.role.value})")
    else:
        print("Hablantes: No disponibles en los datos conservados por X")
    print(f"Enlace: {space.space_url}")
