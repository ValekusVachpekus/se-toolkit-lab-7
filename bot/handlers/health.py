"""Handler for /health command."""

from __future__ import annotations


def handle_health() -> str:
    """Handle /health command — check backend status.
    
    TODO: Implement actual backend health check in Task 2.
    For now, returns placeholder.
    """
    return "Backend status: OK (placeholder — will implement API check in Task 2)"
