# mcp_sdk/shell/composition.py

from __future__ import annotations

from core.dispatcher import Dispatcher
from core.tools import get_tools

# providers (external world adapters)
from providers.pollinations import (
    PollinationsTextClient,
    PollinationsImageClient,
    PollinationsAudioClient,
)


def build_dispatcher() -> Dispatcher:
    """
    Composition root for MCP SDK.

    Rules:
    - This is the ONLY place where providers are instantiated
    - Core must not import providers
    - Shells (CLI / HTTP / STDIO) must call this function
    """

    tools = get_tools()

    ai_executors = {
        # key must match request.ai.provider
        "pollinations": PollinationsTextClient(),
        "pollinations_image": PollinationsImageClient(),
        "pollinations_audio": PollinationsAudioClient(),
    }

    return Dispatcher(
        tools=tools,
        ai_executors=ai_executors,
    )
