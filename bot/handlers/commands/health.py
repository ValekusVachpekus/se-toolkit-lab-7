"""Handler for /health command."""

from __future__ import annotations

import asyncio

from services.lms_api import LmsApiClient, LmsConnectionError, LmsApiException


async def handle_health_async(lms_client: LmsApiClient) -> str:
    """Handle /health command — check backend status.
    
    Args:
        lms_client: LMS API client instance
    
    Returns:
        Health status message
    """
    try:
        items = await lms_client.get_items()
        item_count = len(items) if isinstance(items, list) else 0
        return f"Backend is healthy. {item_count} items available."
    except LmsConnectionError as e:
        return f"Backend error: {e}"
    except LmsApiException as e:
        return f"Backend error: HTTP {e.status_code} {e.message}"


def handle_health() -> str:
    """Handle /health command — synchronous wrapper.
    
    This function creates an async client, runs the health check,
    and returns the result. For production Telegram runtime,
    you would use async handlers directly.
    """
    from config import BotSettings
    
    settings = BotSettings()
    
    async def _check():
        client = LmsApiClient(
            base_url=settings.lms_api_base_url,
            api_key=settings.lms_api_key,
        )
        try:
            return await handle_health_async(client)
        finally:
            await client.close()
    
    return asyncio.run(_check())
