# mcp_sdk/shell/stdio.py

from __future__ import annotations

import sys
from typing import Any, Dict

from protocol.request import MCPRequest
from protocol.response import MCPResponse
from protocol.errors import MCPError, MCPErrorCode

from utils.json import loads as json_loads
from shell.composition import build_dispatcher


def main() -> None:
    """
    STDIO runner for MCP.

    Reads one JSON object per line.
    Writes one JSON response per line.
    """

    dispatcher = build_dispatcher()

    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue

        try:
            payload: Dict[str, Any] = json_loads(raw)
            request = MCPRequest.from_dict(payload)

            response = dispatcher.dispatch(request)

        except MCPError as err:
            response = MCPResponse.error_response(error=err.to_dict())

        except Exception as exc:
            fatal = MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Fatal STDIO error",
                details={"error": str(exc)},
            )
            response = MCPResponse.error_response(error=fatal.to_dict())

        sys.stdout.write(response.to_json() + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
