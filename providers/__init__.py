# mcp_sdk/providers/__init__.py

"""
External providers for MCP SDK.

Providers are adapters to third-party systems (LLMs, image models,
audio models, APIs). They must remain isolated from core logic.

Currently available providers:
- pollinations
"""

from . import pollinations

__all__ = [
    "pollinations",
]
