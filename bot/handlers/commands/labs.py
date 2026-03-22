"""Handler for /labs command."""

from __future__ import annotations

import asyncio

from services.lms_api import LmsApiClient, LmsConnectionError, LmsApiException


async def handle_labs_async(lms_client: LmsApiClient) -> str:
    """Handle /labs command — list available labs.
    
    Args:
        lms_client: LMS API client instance
    
    Returns:
        Formatted list of labs
    """
    try:
        items = await lms_client.get_items()
        
        if not items:
            return "No labs available. The backend may not have synced data yet."
        
        # Filter only labs (not tasks)
        labs = [item for item in items if item.get("type") == "lab"]
        
        if not labs:
            return "No labs found. Check that the backend has lab data."
        
        # Format lab list
        lab_lines = []
        for lab in labs:
            title = lab.get("title", "Unknown Lab")
            lab_lines.append(f"- {title}")
        
        return "Available labs:\n" + "\n".join(lab_lines)
        
    except LmsConnectionError as e:
        return f"Backend error: {e}"
    except LmsApiException as e:
        return f"Backend error: HTTP {e.status_code} {e.message}"


def handle_labs() -> str:
    """Handle /labs command — synchronous wrapper."""
    from config import BotSettings
    
    settings = BotSettings()
    
    async def _fetch():
        client = LmsApiClient(
            base_url=settings.lms_api_base_url,
            api_key=settings.lms_api_key,
        )
        try:
            return await handle_labs_async(client)
        finally:
            await client.close()
    
    return asyncio.run(_fetch())
