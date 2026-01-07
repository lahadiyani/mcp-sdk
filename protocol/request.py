from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class MCPRequest:
    """
    MCPRequest represents a single, stateless protocol request.

    This object is:
    - immutable
    - transport-agnostic
    - tool-agnostic (can call AI-only)
    """

    tool: Optional[str] = None
    input: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)
    ai: Optional[Dict[str, Any]] = None

    # ---------- Constructors ----------

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPRequest":
        """
        Create MCPRequest from raw dictionary input.

        Supports both tool-based and AI-only requests.
        """
        if not isinstance(data, dict):
            raise TypeError("MCPRequest payload must be a dict")

        tool = data.get("tool")
        input_payload = data.get("input")
        meta = data.get("meta", {})
        ai_spec = data.get("ai")

        cls._validate_fields(tool, input_payload, meta, ai_spec)

        return cls(
            tool=tool,
            input=input_payload,
            meta=meta,
            ai=ai_spec,
        )

    # ---------- Validation ----------

    @staticmethod
    def _validate_fields(
        tool: Any,
        input_payload: Any,
        meta: Any,
        ai_spec: Any,
    ) -> None:
        if not isinstance(input_payload, dict):
            raise ValueError("Field 'input' must be a dictionary")

        if not isinstance(meta, dict):
            raise ValueError("Field 'meta' must be a dictionary")

        if tool is not None:
            if not isinstance(tool, str) or not tool.strip():
                raise ValueError("Field 'tool' must be a non-empty string if provided")
        else:
            # jika tool None, harus ada AI spec
            if not isinstance(ai_spec, dict) or not ai_spec:
                raise ValueError("Field 'ai' must be provided if 'tool' is None")

    # ---------- Serialization ----------

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize MCPRequest back to dictionary.
        """
        return {
            "tool": self.tool,
            "input": self.input,
            "meta": self.meta,
            "ai": self.ai,
        }
