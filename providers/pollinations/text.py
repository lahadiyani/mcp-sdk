from __future__ import annotations
import asyncio
from typing import Any, List, Union

import pollinations


class PollinationsTextClient:
    """
    Synchronous wrapper around pollinations.Text.

    Responsibilities:
    - Generate text from prompts
    - Supports streaming and non-streaming modes
    - Bridges async Pollinations SDK to synchronous usage
    """

    def __init__(
        self,
        model: str | None = "openai",
        system: str | None = "You are a helpful AI assistant.",
        json_mode: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Pollinations Text model.

        Args:
            model: Model name (default "openai")
            system: Optional system instruction
            json_mode: Whether to return output in JSON format
            **kwargs: Extra arguments forwarded to pollinations.Text
        """
        self._model = pollinations.Text(
            model=model,
            system=system,
            json_mode=json_mode,
            **kwargs,
        )

    def generate(
        self,
        prompt: str,
        *,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[str, List[str]]:
        """
        Generate text from a prompt.

        Args:
            prompt: Input text prompt
            stream: If True, returns list of tokens
            **kwargs: Extra args passed to pollinations.Text.Async

        Returns:
            str: Full output if stream=False
            List[str]: Tokens if stream=True
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("prompt must be a non-empty string")

        try:
            if stream:
                return self._run_async_stream(prompt, **kwargs)
            return self._run_async(prompt, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Pollinations text generation failed: {e}") from e

    def _run_async(self, prompt: str, **kwargs: Any) -> str:
        """Run non-streaming async generation in blocking mode."""
        return asyncio.run(self._model.Async(prompt, **kwargs))

    def _run_async_stream(self, prompt: str, **kwargs: Any) -> List[str]:
        """
        Run streaming async generation and collect tokens.

        Returns:
            List[str]: List of tokens from the async generator
        """

        async def _stream():
            async for token in await self._model.Async(prompt, stream=True, **kwargs):
                yield token

        return asyncio.run(_collect_stream(_stream()))


async def _collect_stream(async_gen):
    """
    Collect async generator into a list.

    Args:
        async_gen: Async generator of tokens

    Returns:
        List of tokens
    """
    output = []
    async for item in async_gen:
        output.append(item)
    return output
