# mcp_sdk/core/contracts.py

from __future__ import annotations

from typing import Any, Dict, Protocol, runtime_checkable


# -------------------------------------------------
# PURE TOOL CONTRACT
# -------------------------------------------------

@runtime_checkable
class Tool(Protocol):
    """
    Pure tool interface for MCP core.

    A Tool MUST:
    - be stateless
    - be deterministic
    - have no side effects
    - accept dict input
    - return dict output
    """

    name: str

    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        ...


# -------------------------------------------------
# AI EXECUTION CONTRACT (SIDE-EFFECT BOUNDARY)
# -------------------------------------------------

@runtime_checkable
class AIExecutor(Protocol):
    """
    Abstract contract for AI execution.

    Implementations may:
    - call external services
    - be async internally
    - perform IO

    Core MUST treat this as opaque.
    """

    provider: str

    def generate(self, payload: Dict[str, Any]) -> Any:
        ...


# -------------------------------------------------
# PROVIDER METADATA CONTRACT
# -------------------------------------------------

@runtime_checkable
class ProviderInfo(Protocol):
    """
    Optional metadata contract for providers.
    """

    name: str
    capabilities: Dict[str, Any]
