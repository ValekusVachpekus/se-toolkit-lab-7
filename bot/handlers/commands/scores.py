"""Handler for /scores command."""

from __future__ import annotations

import asyncio

from services.lms_api import LmsApiClient, LmsConnectionError, LmsApiException


async def handle_scores_async(lms_client: LmsApiClient, lab_id: str | None = None) -> str:
    """Handle /scores command — get scores for a lab.
    
    Args:
        lms_client: LMS API client instance
        lab_id: The lab identifier (e.g., "lab-04")
    
    Returns:
        Formatted scores response
    """
    if lab_id is None:
        return "Please specify a lab ID. Usage: /scores lab-04"
    
    try:
        # Get pass rates for the lab
        pass_rates = await lms_client.get_pass_rates(lab=lab_id)
        
        if not pass_rates:
            return f"No scores found for {lab_id}. The lab may not have submissions yet."
        
        # Format the response
        lines = [f"Pass rates for {lab_id}:"]
        
        # pass_rates structure: {"lab_id": "...", "pass_rates": [...]}
        rates = pass_rates.get("pass_rates", []) if isinstance(pass_rates, dict) else pass_rates
        
        if not rates:
            return f"No pass rates available for {lab_id}."
        
        for rate in rates:
            task_name = rate.get("task_name", rate.get("task", "Unknown Task"))
            pass_rate = rate.get("pass_rate", rate.get("rate", 0))
            attempts = rate.get("attempts", 0)
            lines.append(f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)")
        
        return "\n".join(lines)
        
    except LmsConnectionError as e:
        return f"Backend error: {e}"
    except LmsApiException as e:
        return f"Backend error: HTTP {e.status_code} {e.message}"


def handle_scores(lab_id: str | None = None) -> str:
    """Handle /scores command — synchronous wrapper."""
    from config import BotSettings
    
    settings = BotSettings()
    
    async def _fetch():
        client = LmsApiClient(
            base_url=settings.lms_api_base_url,
            api_key=settings.lms_api_key,
        )
        try:
            return await handle_scores_async(client, lab_id)
        finally:
            await client.close()
    
    return asyncio.run(_fetch())
