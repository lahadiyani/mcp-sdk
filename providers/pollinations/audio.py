# mcp_sdk/providers/pollinations/audio.py
from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Any

import pollinations


class PollinationsAudioClient:
    """
    Client to retrieve AI responses directly as audio (MP3).

    Responsibilities:
    - Accepts a text prompt
    - Returns the AI answer as an audio file (MP3)
    - Bridges async Pollinations API to sync usage
    """

    def __init__(
        self,
        model: str | None = "openai",
        system: str | None = "You are a helpful AI assistant.",
        **kwargs: Any,
    ) -> None:
        self._model = pollinations.Text(
            model=model,
            system=system,
            **kwargs,
        )

    def generate_audio(
        self,
        prompt: str,
        output_file: str | Path,
        **kwargs: Any,
    ) -> str:
        """
        Generate an audio file (MP3) from an AI text response.

        Args:
            prompt: The text prompt for AI
            output_file: Path to save MP3
            **kwargs: Extra arguments passed to Pollinations

        Returns:
            str: Path to saved MP3 file
        """
        output_file = str(Path(output_file))
        if not prompt or not isinstance(prompt, str):
            raise ValueError("prompt must be a non-empty string")

        try:
            # Gunakan method SpeakAsync atau sejenis untuk text -> audio
            # Hasilnya akan berupa bytes audio yang kita simpan sendiri
            audio_bytes = asyncio.run(self._model.SpeakAsync(prompt, **kwargs))

            # Simpan MP3 ke file
            Path(output_file).write_bytes(audio_bytes)
            return output_file
        except Exception as e:
            raise RuntimeError(f"Pollinations audio generation failed: {e}") from e
