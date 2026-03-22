"""LMS Telegram Bot — Entry point.

Supports:
- CLI test mode: uv run bot.py --test "message"
- Telegram bot runtime (aiogram)
- Intent-based natural language routing via LLM
"""

from __future__ import annotations

import argparse

from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
    route_intent,
)

# Inline keyboard buttons for common actions
INLINE_KEYBOARD_BUTTONS = [
    [{"text": "📚 Available Labs", "callback_data": "labs"}, {"text": "🏥 Health Check", "callback_data": "health"}],
    [{"text": "📊 Scores lab-04", "callback_data": "scores_lab-04"}, {"text": "📊 Scores lab-01", "callback_data": "scores_lab-01"}],
    [{"text": "❓ Help", "callback_data": "help"}],
]


def dispatch_test_command(command_text: str) -> str:
    """Dispatch a command string to the appropriate handler.
    
    For plain text (not starting with /), use LLM intent routing.
    
    Args:
        command_text: The command or message text
    
    Returns:
        The handler's response text
    """
    text = command_text.strip()
    
    # Slash commands — direct routing
    if text.startswith("/start"):
        return handle_start()
    elif text.startswith("/help"):
        return handle_help()
    elif text.startswith("/health"):
        return handle_health()
    elif text.startswith("/labs"):
        return handle_labs()
    elif text.startswith("/scores"):
        # Extract lab_id if provided: /scores lab-04
        parts = text.split(maxsplit=1)
        lab_id = parts[1] if len(parts) > 1 else None
        return handle_scores(lab_id)
    elif text.startswith("/"):
        # Unknown slash command
        return "Unknown command. Use /help to see available commands."
    else:
        # Plain text — use LLM intent routing
        return route_intent(text)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        dest="test_command",
        help="Run command in CLI test mode (e.g., --test '/start' or --test 'what labs are available')",
    )
    args = parser.parse_args()

    if args.test_command is not None:
        print(dispatch_test_command(args.test_command))
        return 0

    # Telegram runtime — not implemented in this task
    print("Telegram runtime is not implemented yet. Use --test mode.")
    print("Example: uv run bot.py --test 'what labs are available?'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
