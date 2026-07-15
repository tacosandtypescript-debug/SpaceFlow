from __future__ import annotations

import os
import sys
from typing import TextIO


RESET = "0"
BOLD = "1"
DIM = "2"
RED = "31"
GREEN = "32"
YELLOW = "33"
CYAN = "36"
BRIGHT_CYAN = "96"


def colors_enabled(stream: TextIO | None = None) -> bool:
    stream = stream or sys.stdout
    if "NO_COLOR" in os.environ or os.environ.get("TERM", "").lower() == "dumb":
        return False
    if os.environ.get("SPACEFLOW_COLOR") == "1":
        return True
    return bool(getattr(stream, "isatty", lambda: False)())


def paint(text: object, *codes: str, stream: TextIO | None = None) -> str:
    value = str(text)
    if not codes or not colors_enabled(stream):
        return value
    return f"\033[{';'.join(codes)}m{value}\033[{RESET}m"


def success(message: object) -> str:
    return paint(f"✓ {message}", GREEN)


def warning(message: object) -> str:
    return paint(f"! {message}", YELLOW)


def error(message: object) -> str:
    return paint(f"✗ {message}", RED)
