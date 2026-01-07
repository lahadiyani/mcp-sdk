# mcp_sdk/protocol/response.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class MCPResponse:
    """
    MCPResponse represents a single, stateless protocol response.

    This object is:
    - immutable
    - serializable
    - transport-agnostic
    """

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    # ---------- Constructors ----------

    @classmethod
    def success_response(
        cls,
        data: Dict[str, Any],
        meta: Optional[Dict[str, Any]] = None,
    ) -> "MCPResponse":
        if not isinstance(data, dict):
            raise TypeError("Success response data must be a dict")

        return cls(
            success=True,
            data=data,
            error=None,
            meta=meta or {},
        )

    @classmethod
    def error_response(
        cls,
        error: Dict[str, Any],
        meta: Optional[Dict[str, Any]] = None,
    ) -> "MCPResponse":
        if not isinstance(error, dict):
            raise TypeError("Error response must be a dict")

        return cls(
            success=False,
            data=None,
            error=error,
            meta=meta or {},
        )

    # ---------- Validation ----------

    def __post_init__(self) -> None:
        if self.success:
            if self.data is None:
                raise ValueError("Success response must include 'data'")
            if self.error is not None:
                raise ValueError("Success response cannot include 'error'")
        else:
            if self.error is None:
                raise ValueError("Error response must include 'error'")
            if self.data is not None:
                raise ValueError("Error response cannot include 'data'")

        if not isinstance(self.meta, dict):
            raise ValueError("Field 'meta' must be a dictionary")

    # ---------- Serialization ----------

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize MCPResponse to dictionary.
        """
        payload = {
            "success": self.success,
            "meta": self.meta,
        }

        if self.success:
            payload["data"] = self.data
        else:
            payload["error"] = self.error

        return payload
