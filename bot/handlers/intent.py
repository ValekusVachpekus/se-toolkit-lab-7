"""Intent-based natural language router.

This handler uses an LLM to understand user intent and call appropriate tools.
"""

from __future__ import annotations

import asyncio

from services.llm_client import LlmClient, TOOL_DEFINITIONS, SYSTEM_PROMPT
from services.lms_api import LmsApiError


async def route_intent_async(llm_client: LlmClient, user_message: str) -> str:
    """Route user message to appropriate tools via LLM.
    
    Args:
        llm_client: LLM client instance
        user_message: User's natural language message
    
    Returns:
        Formatted response
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    
    try:
        response = await llm_client.chat_with_tools(
            messages=messages,
            tools=TOOL_DEFINITIONS,
            max_iterations=5,
        )
        return response
    except Exception as e:
        # Handle LLM errors gracefully
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            return "LLM authentication error. The API token may have expired. Please check the LLM_API_KEY."
        elif "connection" in error_msg.lower():
            return f"LLM connection error: {error_msg}. Check that the LLM service is running."
        else:
            return f"LLM error: {error_msg}"


def route_intent(user_message: str) -> str:
    """Route user message — synchronous wrapper.
    
    Args:
        user_message: User's natural language message
    
    Returns:
        Formatted response
    """
    from config import BotSettings
    
    settings = BotSettings()
    
    async def _route():
        client = LlmClient(
            base_url=settings.llm_api_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_api_model if hasattr(settings, 'llm_api_model') else "qwen3-coder-flash",
        )
        try:
            return await route_intent_async(client, user_message)
        finally:
            await client.close()
    
    return asyncio.run(_route())
