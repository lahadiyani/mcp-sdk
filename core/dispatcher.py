# mcp_sdk/core/dispatcher.py

from __future__ import annotations

from typing import Dict, Optional, Any

from protocol.request import MCPRequest
from protocol.response import MCPResponse
from protocol.errors import MCPError, MCPErrorCode
from protocol.schema import MCPSchema

from core.contracts import Tool, AIExecutor


class Dispatcher:
    """
    Stateless dispatcher that routes MCPRequest to tools or AI executors.
    """

    def __init__(
        self,
        tools: Dict[str, Tool],
        ai_executors: Optional[Dict[str, AIExecutor]] = None,
    ) -> None:
        self._tools = tools
        self._ai_executors = ai_executors or {}

    # -------------------------------------------------

    def dispatch(self, request: MCPRequest) -> MCPResponse:
        """
        Route MCPRequest to the appropriate execution path.
        """
        try:
            MCPSchema.validate_request(request)

            if getattr(request, "ai", None) is not None:
                result = self._dispatch_ai(request)

                ai_type = request.ai.get("type")
                if ai_type == "text":
                    payload = {"text": result}
                elif ai_type == "image":
                    payload = {"image": result}
                elif ai_type == "audio":
                    # audio executors may return path or text depending on impl
                    payload = {"audio": result}
                else:
                    raise MCPError(
                        code=MCPErrorCode.SCHEMA_VIOLATION,
                        message="Invalid AI task type",
                    )
            else:
                payload = self._dispatch_tool(request)

            return MCPResponse.success_response(data=payload)

        except MCPError as err:
            return MCPResponse.error_response(error=err.to_dict())

        except Exception as exc:
            internal = MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Internal error occurred",
                details={"error": str(exc)},
            )
            return MCPResponse.error_response(error=internal.to_dict())

    # -------------------------------------------------
    # Internal routing
    # -------------------------------------------------

    def _dispatch_tool(self, request: MCPRequest) -> Dict[str, Any]:
        if not request.tool:
            raise MCPError(
                code=MCPErrorCode.INVALID_REQUEST,
                message="Tool name is required for tool execution",
            )
        tool = self._get_tool(request.tool)
        return tool.execute(request.input)

    def _dispatch_ai(self, request: MCPRequest) -> Any:
        ai_spec = request.ai or {}
        provider_name = ai_spec.get("provider")

        if not provider_name:
            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="AI 'provider' must be specified",
            )

        executor = self._get_ai_executor(provider_name)

        ai_type = ai_spec.get("type")
        # extra kwargs from ai spec (provider-level hints)
        extra_kwargs = {k: v for k, v in ai_spec.items() if k not in ("provider", "type")}
        # forward relevant kwargs from request.input (e.g. save_to_file, file_path, negative_prompt, output_file)
        input_kwargs = {k: v for k, v in request.input.items() if k != "prompt"}

        if ai_type in ("text", "image"):
            prompt = request.input.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise MCPError(
                    code=MCPErrorCode.SCHEMA_VIOLATION,
                    message="Prompt must be a non-empty string in request.input['prompt']",
                )

            # merge kwargs: input-level take precedence over ai_spec
            call_kwargs = {**extra_kwargs, **input_kwargs}

            if hasattr(executor, "generate"):
                return executor.generate(prompt, **call_kwargs)
            elif hasattr(executor, "generate_async"):
                return executor.generate_async(prompt, **call_kwargs)
            else:
                raise MCPError(
                    code=MCPErrorCode.TOOL_ERROR,
                    message=f"AI executor for '{provider_name}' does not support text/image generation",
                )

        if ai_type == "audio":
            prompt = request.input.get("prompt")
            file_path = request.input.get("file_path")

            # Case A: generate audio from prompt -> save to file
            if isinstance(prompt, str) and prompt.strip() and file_path:
                call_kwargs = {**extra_kwargs, **input_kwargs}
                if hasattr(executor, "generate_audio"):
                    return executor.generate_audio(prompt, output_file=file_path, **call_kwargs)
                if hasattr(executor, "generate"):
                    return executor.generate(prompt, output_file=file_path, **call_kwargs)
                raise MCPError(
                    code=MCPErrorCode.TOOL_ERROR,
                    message=f"AI executor for '{provider_name}' does not support audio generation to file",
                )

            # Case B: transcribe existing file -> return text
            if file_path and not prompt:
                if hasattr(executor, "transcribe"):
                    return executor.transcribe(file_path, **{**extra_kwargs, **input_kwargs})
                raise MCPError(
                    code=MCPErrorCode.TOOL_ERROR,
                    message=f"AI executor for '{provider_name}' does not support audio transcription",
                )

            raise MCPError(
                code=MCPErrorCode.SCHEMA_VIOLATION,
                message="For audio tasks provide either 'prompt' and 'file_path' (generate) or 'file_path' only (transcribe)",
            )

        raise MCPError(
            code=MCPErrorCode.SCHEMA_VIOLATION,
            message="Invalid AI task type",
        )

    # -------------------------------------------------
    # Registry helpers
    # -------------------------------------------------

    def _get_tool(self, name: str) -> Tool:
        tool = self._tools.get(name)
        if tool is None:
            raise MCPError(
                code=MCPErrorCode.TOOL_NOT_FOUND,
                message=f"Tool not found: {name}",
            )
        return tool

    def _get_ai_executor(self, provider: str) -> AIExecutor:
        executor = self._ai_executors.get(provider)
        if executor is None:
            raise MCPError(
                code=MCPErrorCode.TOOL_NOT_FOUND,
                message=f"AI provider not found: {provider}",
            )
        return executor
