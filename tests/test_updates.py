from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from spaceflow.application.ports import ReleaseInfo
from spaceflow.application.update_service import UpdateService
from spaceflow.domain.errors import UpdateFailed
from spaceflow.infrastructure.updater import GitHubReleaseRepository, version_tuple


class Releases:
    def __init__(self, release):
        self.release = release
        self.calls = 0

    def latest(self):
        self.calls += 1
        return self.release

    def install(self, release):
        self.installed = release


class State:
    def __init__(self):
        self.value = None

    def get_last_update_check(self):
        return self.value

    def set_last_update_check(self, value):
        self.value = value


class UpdateTests(unittest.TestCase):
    def test_semantic_versions(self):
        self.assertGreater(version_tuple("v1.10.0"), version_tuple("1.2.9"))

    def test_daily_check_is_throttled(self):
        release = ReleaseInfo("0.2.0", "asset", "sum", "page")
        repository = Releases(release)
        state = State()
        service = UpdateService(repository, state)
        self.assertEqual(service.check(), release)
        self.assertIsNone(service.check())
        self.assertEqual(repository.calls, 1)

    def test_checksum_parser(self):
        text = "abc123  other.txt\ndeadbeef  spaceflow.pyz\n"
        self.assertEqual(GitHubReleaseRepository._expected_hash(text), "deadbeef")
        with self.assertRaises(UpdateFailed):
            GitHubReleaseRepository._expected_hash("deadbeef other.txt")


if __name__ == "__main__":
    unittest.main()
