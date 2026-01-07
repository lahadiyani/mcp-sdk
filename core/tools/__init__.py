# mcp_sdk/core/tools/__init__.py

from __future__ import annotations

from typing import Dict

from core.contracts import Tool
from core.tools.generate import GenerateTextTool
from core.tools.validate import ValidateInputTool


def get_tools() -> Dict[str, Tool]:
    """
    Return registry of available MCP tools.

    This function is:
    - explicit
    - deterministic
    - side-effect free
    """
    tools = [
        GenerateTextTool(),
        ValidateInputTool(),
    ]

    return {tool.name: tool for tool in tools}
