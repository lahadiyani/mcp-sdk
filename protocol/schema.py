# mcp_sdk/protocol/schema.py

from __future__ import annotations

from typing import Any, Dict, Optional, Literal

from .request import MCPRequest
from .errors import MCPError, MCPErrorCode


# ---- AI SCHEMA DEFINITIONS (PROTOCOL-LEVEL) -----------------

AIType = Literal["text", "image", "audio"]


class AITaskSchema:
    """
    Schema definition for optional AI task metadata.

    This schema describes WHAT kind of AI task is requested,
    not HOW it is executed or by whom.
    """

    REQUIRED_FIELDS = {"type"}
    OPTIONAL_FIELDS = {"provider", "model", "params"}

    @staticmethod
    def validate(ai: Dict[str, Any]) -> None:
        if not isinstance(ai, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="AI field must be an object",
            )

        # required: type
        task_type = ai.get("type")
        if task_type not in ("text", "image", "audio"):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Invalid AI task type",
                details={"allowed": ["text", "image", "audio"]},
            )

        # optional: provider
        if "provider" in ai and not isinstance(ai["provider"], str):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="AI provider must be a string",
            )

        # optional: model
        if "model" in ai and not isinstance(ai["model"], str):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="AI model must be a string",
            )

        # optional: params
        if "params" in ai and not isinstance(ai["params"], dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="AI params must be an object",
            )


# ---- MCP SCHEMA VALIDATOR -----------------------------------

class MCPSchema:
    """
    Protocol-level schema validator.

    Validates MCPRequest structure and basic constraints.
    """

    @staticmethod
    def validate_request(request: MCPRequest) -> None:
        """
        Validate MCPRequest against protocol schema.

        Raises:
            MCPError on schema violation
        """

        # --- tool name constraints ---
        if not request.tool or not request.tool.isidentifier():
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Tool name must be a valid identifier",
                details={"tool": request.tool},
            )

        # --- input payload constraints ---
        MCPSchema._validate_input_payload(request.input)

        # --- meta constraints (optional) ---
        if request.meta is not None and not isinstance(request.meta, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Meta must be a dictionary if provided",
            )

        # --- AI task constraints (optional) ---
        if getattr(request, "ai", None) is not None:
            AITaskSchema.validate(request.ai)

    @staticmethod
    def _validate_input_payload(payload: Any) -> None:
        if not isinstance(payload, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Input payload must be an object",
            )

        # defensive size guard
        if len(payload) > 100:
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Input payload too large",
                details={"max_fields": 100},
            )
