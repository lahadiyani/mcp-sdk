# mcp_sdk/utils/logging.py

from __future__ import annotations

import logging
import sys
from typing import Optional, TextIO


DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%dT%H:%M:%S"


def get_logger(
    name: str,
    *,
    level: int = logging.INFO,
    stream: Optional[TextIO] = None,
) -> logging.Logger:
    """
    Return a configured logger instance.

    Guarantees:
    - idempotent (safe to call multiple times)
    - no duplicate handlers
    - deterministic format
    - no global logging side-effects
    """

    logger = logging.getLogger(name)

    # Always enforce level (important!)
    logger.setLevel(level)

    # Resolve stream explicitly
    output = stream if stream is not None else sys.stderr

    # Check for compatible existing handler
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream is output:
                return logger

    # Create new handler only if needed
    handler = logging.StreamHandler(output)
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            fmt=DEFAULT_FORMAT,
            datefmt=DEFAULT_DATEFMT,
        )
    )

    logger.addHandler(handler)
    logger.propagate = False

    return logger
