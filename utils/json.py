# mcp_sdk/utils/json.py

from __future__ import annotations

import json
from typing import Any


class JSONError(ValueError):
    """Raised when JSON parsing or serialization fails."""


def loads(raw: str) -> dict[str, Any]:
    """
    Parse JSON string into dict.

    Rules:
    - input must be valid JSON object
    - no silent fallback
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise JSONError(str(e)) from e

    if not isinstance(data, dict):
        raise JSONError("JSON root must be an object")

    return data


def dumps(data: Any, pretty: bool = False) -> str:
    try:
        if pretty:
            return json.dumps(data, ensure_ascii=False, indent=2)
        else:
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError) as e:
        raise JSONError(str(e)) from e
