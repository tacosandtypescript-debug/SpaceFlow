from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from spaceflow.application.ports import ReleaseInfo, UpdateRepository, UpdateStateStore


@dataclass(slots=True)
class UpdateService:
    repository: UpdateRepository
    state_store: UpdateStateStore

    def check(self, force: bool = False) -> ReleaseInfo | None:
        now = datetime.now(timezone.utc)
        previous = self.state_store.get_last_update_check()
        if not force and previous and now - previous < timedelta(hours=24):
            return None
        release = self.repository.latest()
        self.state_store.set_last_update_check(now)
        return release

    def install(self, release: ReleaseInfo) -> None:
        self.repository.install(release)
