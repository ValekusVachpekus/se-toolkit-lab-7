"""Services for the LMS Telegram bot.

Services are external API clients (LMS backend, LLM provider).
They handle HTTP requests, authentication, and error handling.
"""

from __future__ import annotations

from .lms_api import (
    LmsApiClient,
    LmsApiError,
    LmsConnectionError,
    LmsApiException,
)
from .llm_client import (
    LlmClient,
    TOOL_DEFINITIONS,
    SYSTEM_PROMPT,
)

__all__ = [
    "LmsApiClient",
    "LmsApiError",
    "LmsConnectionError",
    "LmsApiException",
    "LlmClient",
    "TOOL_DEFINITIONS",
    "SYSTEM_PROMPT",
]
