from __future__ import annotations

import http.cookiejar
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from spaceflow.domain.errors import InvalidSpaceUrl


SPACE_PATH = re.compile(r"/(?:i/)?spaces/([A-Za-z0-9]{1,32})", re.IGNORECASE)
STATUS_PATH = re.compile(r"/[^/]+/status/(\d+)", re.IGNORECASE)
SPACE_IN_TEXT = re.compile(r"(?:https?:)?(?:\\?/\\?/)?(?:www\.)?(?:x|twitter)\.com\\?/i\\?/spaces\\?/([A-Za-z0-9]{1,32})", re.IGNORECASE)


class XSpaceUrlResolver:
    def __init__(self, cookies_file: Path, timeout: int = 20) -> None:
        self.cookies_file = cookies_file
        self.timeout = timeout

    def resolve(self, url: str) -> str:
        cleaned = url.strip().strip("<>")
        parsed = urlparse(cleaned)
        host = parsed.netloc.lower().split(":", 1)[0]
        if host.startswith("www."):
            host = host[4:]
        if host not in {"x.com", "twitter.com", "mobile.twitter.com"}:
            raise InvalidSpaceUrl("Usa un enlace de x.com o twitter.com")
        direct = SPACE_PATH.search(parsed.path)
        if direct:
            return f"https://x.com/i/spaces/{direct.group(1)}"
        status = STATUS_PATH.search(parsed.path)
        if not status:
            raise InvalidSpaceUrl("El enlace no es una publicación ni un Space de X")

        for payload in self._status_payloads(cleaned, status.group(1)):
            space_id = self._find_space_id(payload)
            if space_id:
                return f"https://x.com/i/spaces/{space_id}"
        raise InvalidSpaceUrl(
            "X no reveló el Space enlazado. Abre la publicación y copia el enlace de “Reproducir grabación”."
        )

    def _status_payloads(self, original_url: str, status_id: str) -> Iterable[Any]:
        urls = (
            original_url,
            f"https://cdn.syndication.twimg.com/tweet-result?id={status_id}&lang=es",
            f"https://publish.twitter.com/oembed?url=https://x.com/i/status/{status_id}",
        )
        opener = self._opener()
        for candidate in urls:
            request = urllib.request.Request(
                candidate,
                headers={
                    "User-Agent": "Mozilla/5.0 (SpaceFlow/0.1; +https://github.com/tacosandtypescript-debug/SpaceFlow)",
                    "Accept": "text/html,application/json",
                },
            )
            try:
                with opener.open(request, timeout=self.timeout) as response:
                    body = response.read().decode("utf-8", errors="replace")
            except (OSError, urllib.error.URLError):
                continue
            yield body
            try:
                yield json.loads(body)
            except json.JSONDecodeError:
                pass

    def _opener(self) -> urllib.request.OpenerDirector:
        jar = http.cookiejar.MozillaCookieJar(str(self.cookies_file))
        try:
            jar.load(ignore_discard=True, ignore_expires=True)
        except (OSError, http.cookiejar.LoadError):
            pass
        return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    @classmethod
    def _find_space_id(cls, payload: Any) -> str | None:
        if isinstance(payload, str):
            normalized = payload.replace("\\u002F", "/").replace("\\/", "/")
            match = SPACE_IN_TEXT.search(normalized) or SPACE_PATH.search(normalized)
            return match.group(1) if match else None
        if isinstance(payload, dict):
            for key, value in payload.items():
                if key.lower() in {"space_id", "spaceid"} and isinstance(value, str) and value.isalnum():
                    return value
                found = cls._find_space_id(value)
                if found:
                    return found
        if isinstance(payload, list):
            for value in payload:
                found = cls._find_space_id(value)
                if found:
                    return found
        return None
