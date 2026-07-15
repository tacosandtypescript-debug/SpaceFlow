from __future__ import annotations

import unittest
from pathlib import Path

from spaceflow.domain.errors import InvalidSpaceUrl
from spaceflow.infrastructure.resolver import XSpaceUrlResolver


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.resolver = XSpaceUrlResolver(Path("missing-cookies.txt"))

    def test_direct_x_space(self):
        result = self.resolver.resolve("https://x.com/i/spaces/1nxnRRdLWNexO?s=46")
        self.assertEqual(result, "https://x.com/i/spaces/1nxnRRdLWNexO")

    def test_direct_twitter_space(self):
        result = self.resolver.resolve("https://twitter.com/i/spaces/AbC123")
        self.assertEqual(result, "https://x.com/i/spaces/AbC123")

    def test_space_id_is_found_in_escaped_html(self):
        payload = r'{"expanded_url":"https:\/\/x.com\/i\/spaces\/1nxnRRdLWNexO"}'
        self.assertEqual(self.resolver._find_space_id(payload), "1nxnRRdLWNexO")

    def test_space_id_is_found_recursively(self):
        payload = {"card": {"space_id": "AbC123"}}
        self.assertEqual(self.resolver._find_space_id(payload), "AbC123")

    def test_rejects_untrusted_hosts(self):
        with self.assertRaises(InvalidSpaceUrl):
            self.resolver.resolve("https://example.com/i/spaces/AbC123")


if __name__ == "__main__":
    unittest.main()
