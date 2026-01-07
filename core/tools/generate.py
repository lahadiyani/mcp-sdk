# mcp_sdk/core/tools/generate.py

from __future__ import annotations

from typing import Any, Dict

from core.contracts import Tool
from protocol.errors import MCPError, MCPErrorCode


class GenerateTextTool:
    """
    Example PURE MCP tool.

    This tool:
    - is stateless
    - deterministic
    - performs simple text generation logic
    """

    name = "ai"

    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(input, dict):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Input must be a dictionary",
            )

        prompt = input.get("prompt")

        if not isinstance(prompt, str):
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Field 'prompt' must be a string",
            )

        if not prompt.strip():
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Field 'prompt' cannot be empty",
            )

        # PURE deterministic transformation
        generated_text = self._generate(prompt)

        return {
            "text": generated_text
        }

    # ---------- Internal pure helper ----------

    def _generate(self, prompt: str) -> str:
        """
        Deterministic text generation.

        This is NOT AI. This is a placeholder transformation.
        """
        return f"Generated response: {prompt}"
