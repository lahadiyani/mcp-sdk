from __future__ import annotations

import sys
from typing import Any, Dict

from protocol.request import MCPRequest
from protocol.response import MCPResponse
from protocol.errors import MCPError, MCPErrorCode

from utils.json import loads as json_loads, dumps as json_dumps
from shell.composition import build_dispatcher


# -------------------------------------------------
# IO helpers
# -------------------------------------------------

def read_stdin() -> Dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        raise MCPError(
            code=MCPErrorCode.SCHEMA_VIOLATION,
            message="No input provided on stdin",
        )

    try:
        return json_loads(raw)
    except Exception as exc:
        raise MCPError(
            code=MCPErrorCode.SCHEMA_VIOLATION,
            message="Invalid JSON input",
            details={"error": str(exc)},
        )


def write_stdout(obj: Any) -> None:
    """Tulis output ke stdout menggunakan utils.json.dumps"""
    try:
        sys.stdout.write(json_dumps(obj))
    except Exception as exc:
        # fallback fatal error jika json_dumps gagal
        fatal = MCPError(
            code=MCPErrorCode.INTERNAL_ERROR,
            message="Failed to serialize output JSON",
            details={"error": str(exc)},
        )
        sys.stdout.write(json_dumps(MCPResponse.error_response(error=fatal.to_dict()).to_dict()))


# -------------------------------------------------
# Entry point
# -------------------------------------------------

def main() -> None:
    try:
        payload = read_stdin()
        request = MCPRequest.from_dict(payload)

        dispatcher = build_dispatcher()
        response: MCPResponse = dispatcher.dispatch(request)

        write_stdout(response.to_dict())

    except MCPError as err:
        write_stdout(MCPResponse.error_response(error=err.to_dict()).to_dict())

    except Exception as exc:
        fatal = MCPError(
            code=MCPErrorCode.INTERNAL_ERROR,
            message="Fatal CLI error",
            details={"error": str(exc)},
        )
        write_stdout(MCPResponse.error_response(error=fatal.to_dict()).to_dict())


if __name__ == "__main__":
    main()
