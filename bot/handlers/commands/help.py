"""Handler for /help command."""

from __future__ import annotations


def handle_help() -> str:
    """Handle /help command — list all available commands."""
    return """Available commands:
/start — Welcome message and introduction
/help — Show this help message with all commands
/health — Check backend system status
/labs — List available labs
/scores <lab_id> — Get scores for a specific lab

You can also ask questions in plain language (coming soon)."""
