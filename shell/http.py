from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

from protocol.request import MCPRequest
from protocol.response import MCPResponse
from protocol.errors import MCPError, MCPErrorCode

from shell.composition import build_dispatcher
from utils.json import dumps as json_dumps


# -------------------------------------------------
# HTTP Handler
# -------------------------------------------------

class MCPHandler(BaseHTTPRequestHandler):
    """
    Minimal HTTP handler for MCP protocol.

    Endpoint:
    POST /mcp
    """

    dispatcher = build_dispatcher()

    def do_POST(self) -> None:
        if self.path != "/mcp":
            self._send_error(
                MCPError(
                    code=MCPErrorCode.TOOL_NOT_FOUND,
                    message="Endpoint not found",
                )
            )
            return

        try:
            payload = self._read_json_body()
            request = MCPRequest.from_dict(payload)
            response = self.dispatcher.dispatch(request)

        except MCPError as err:
            response = MCPResponse.error_response(error=err.to_dict())

        except Exception as exc:
            fatal = MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Fatal HTTP error",
                details={"error": str(exc)},
            )
            response = MCPResponse.error_response(error=fatal.to_dict())

        self._send_response(response)

    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    def _read_json_body(self) -> Dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if not length_header:
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Missing Content-Length header",
            )

        try:
            length = int(length_header)
        except ValueError:
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Invalid Content-Length header",
            )

        raw = self.rfile.read(length).decode("utf-8")
        try:
            return MCPRequest._json_loads(raw)  # bisa pakai util json nanti
        except Exception as exc:
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="Invalid JSON body",
                details={"error": str(exc)},
            )

    def _send_response(self, response: MCPResponse) -> None:
        body = json_dumps(response.to_dict()).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, error: MCPError) -> None:
        response = MCPResponse.error_response(error=error.to_dict())
        self._send_response(response)

    def log_message(self, *_: object) -> None:
        # silence default noisy logging
        return


# -------------------------------------------------
# Server bootstrap
# -------------------------------------------------

def run(host: str = "127.0.0.1", port: int = 3333) -> None:
    server = HTTPServer((host, port), MCPHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
