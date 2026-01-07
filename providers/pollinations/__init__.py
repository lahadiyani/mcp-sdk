# mcp_sdk/providers/pollinations/__init__.py

"""
Pollinations provider adapters.

This package exposes thin, synchronous adapters over the
pollinations Python SDK.

Public API:
- PollinationsTextClient
- PollinationsImageClient
- PollinationsAudioClient
"""

from .text import PollinationsTextClient
from .image import PollinationsImageClient
from .audio import PollinationsAudioClient

__all__ = [
    "PollinationsTextClient",
    "PollinationsImageClient",
    "PollinationsAudioClient",
]
