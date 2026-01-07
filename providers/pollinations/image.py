from __future__ import annotations
import asyncio
import tempfile
from pathlib import Path
from typing import Any

import pollinations
from PIL.Image import Image as PILImage


class PollinationsImageClient:
    """
    Synchronous wrapper around pollinations.Image.
    """

    def __init__(
        self,
        model: str | None = "flux",
        width: int = 1024,
        height: int = 1024,
        seed: str | int | None = "random",
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        **kwargs: Any,
    ) -> None:
        self._model = pollinations.Image(
            model=model,
            width=width,
            height=height,
            seed=seed,
            nologo=nologo,
            private=private,
            enhance=enhance,
            safe=safe,
            **kwargs,
        )

    def generate(
        self,
        prompt: str,
        *,
        negative: str = "",
        model: str = "flux",
        save_to_file: bool = False,
        file_path: str | None = None,
        **kwargs: Any,
    ) -> PILImage | str:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image
            negative: Optional negative prompt
            save_to_file: If True, image is saved to disk
            file_path: Optional path to save image (if None, uses temp file)
            **kwargs: Extra args passed to pollinations.Image.Async

        Returns:
            PIL.Image.Image if save_to_file is False,
            else str path to saved image
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("prompt must be a non-empty string")

        try:
            image = self._run_async(prompt, negative=negative, model=model, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Pollinations image generation failed: {e}") from e

        if save_to_file:
            if file_path is None:
                tmp_file = tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                )
                file_path = tmp_file.name
                tmp_file.close()
            else:
                file_path = str(Path(file_path))

            image.save(file_path, format="PNG")
            return file_path

        return image

    def _run_async(self, prompt: str, **kwargs: Any) -> PILImage:
        """
        Internal helper to run async image generation in a blocking manner.
        """
        return asyncio.run(self._model.Async(prompt, **kwargs))
