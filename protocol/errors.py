# protocol/errors.py

from __future__ import annotations
from typing import Any, Dict, Optional
from enum import Enum

class MCPErrorCode(str, Enum):
    INVALID_REQUEST = "INVALID_REQUEST"
    SCHEMA_VIOLATION = "SCHEMA_VIOLATION"
    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    TOOL_ERROR = "TOOL_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class MCPError(Exception):
    """Protocol-level exception."""

    def __init__(self, code: MCPErrorCode, message: str, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.details = details

        super().__init__(f"{code.value}: {message}")

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "code": self.code.value,
            "message": self.message,
        }
        if self.details is not None:
            payload["details"] = self.details
        return payload
