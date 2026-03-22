"""Command handlers for the LMS Telegram bot.

Handlers are plain functions that take input and return text.
They don't know about Telegram — same logic works from --test mode,
unit tests, or Telegram.
"""

from __future__ import annotations


def handle_start() -> str:
    """Handle /start command — welcome message."""
    return "Welcome to LMS Bot! I can help you check your lab scores, view available labs, and monitor system health. Use /help to see all available commands."


def handle_help() -> str:
    """Handle /help command — list all available commands."""
    return """Available commands:
/start — Welcome message and introduction
/help — Show this help message with all commands
/health — Check backend system status
/labs — List available labs
/scores <lab_id> — Get scores for a specific lab

You can also ask questions in plain language (coming soon)."""


def handle_health() -> str:
    """Handle /health command — check backend status.
    
    TODO: Implement actual backend health check in Task 2.
    For now, returns placeholder.
    """
    return "Backend status: OK (placeholder — will implement API check in Task 2)"


def handle_labs() -> str:
    """Handle /labs command — list available labs.
    
    TODO: Implement actual backend API call in Task 2.
    For now, returns placeholder.
    """
    return "Available labs:\n- lab-01: Introduction\n- lab-02: Setup\n- lab-03: Testing\n- lab-04: Deployment\n\n(placeholder — will fetch from API in Task 2)"


def handle_scores(lab_id: str | None = None) -> str:
    """Handle /scores command — get scores for a lab.
    
    Args:
        lab_id: The lab identifier (e.g., "lab-04")
    
    TODO: Implement actual backend API call in Task 2.
    For now, returns placeholder.
    """
    if lab_id is None:
        return "Please specify a lab ID. Usage: /scores lab-04"
    return f"Scores for {lab_id}:\n- Task 1: 80%\n- Task 2: 75%\n- Task 3: 90%\n\n(placeholder — will fetch from API in Task 2)"
