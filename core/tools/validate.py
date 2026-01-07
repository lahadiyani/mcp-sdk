# mcp_sdk/core/tools/validate.py

from __future__ import annotations

from typing import Any, Dict, List

from core.contracts import Tool
from protocol.errors import MCPError, MCPErrorCode


class ValidateInputTool:
    """
    PURE validation tool.

    This tool:
    - does NOT block execution
    - does NOT know business rules
    - only reports validation results
    """

    name = "validate_input"

    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(input, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Input must be a dictionary",
            )

        fields = input.get("fields")
        required = input.get("required", [])

        if not isinstance(fields, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Field 'fields' must be a dictionary",
            )

        if not isinstance(required, list):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Field 'required' must be a list",
            )

        errors: List[str] = []

        for key in required:
            if key not in fields:
                errors.append(f"Missing required field: {key}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }
