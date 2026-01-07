# mcp_sdk/__init__.py

"""
MCP SDK

A stateless, protocol-first Model Context Protocol SDK.

This package exposes only the stable public API.
Internal modules are not re-exported by default.
"""

__author__ = "Hadiani"
__version__ = "0.1.0"
from .core.dispatcher import Dispatcher
from .protocol.request import MCPRequest
from .protocol.response import MCPResponse
from .protocol.errors import MCPError, MCPErrorCode

__all__ = [
    "__version__", "__author__", "Dispatcher", "MCPRequest", "MCPResponse", "MCPError", "MCPErrorCode",
]
