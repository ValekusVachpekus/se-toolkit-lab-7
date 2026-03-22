from __future__ import annotations

import argparse

from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)


def dispatch_test_command(command_text: str) -> str:
    """Dispatch a command string to the appropriate handler.
    
    Args:
        command_text: The command string (e.g., "/start", "/help", "/scores lab-04")
    
    Returns:
        The handler's response text
    """
    command = command_text.strip()
    
    if command.startswith("/start"):
        return handle_start()
    elif command.startswith("/help"):
        return handle_help()
    elif command.startswith("/health"):
        return handle_health()
    elif command.startswith("/labs"):
        return handle_labs()
    elif command.startswith("/scores"):
        # Extract lab_id if provided: /scores lab-04
        parts = command.split(maxsplit=1)
        lab_id = parts[1] if len(parts) > 1 else None
        return handle_scores(lab_id)
    else:
        return "Unknown command. Use /help to see available commands."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", dest="test_command", help="Run command in CLI test mode")
    args = parser.parse_args()

    if args.test_command is not None:
        print(dispatch_test_command(args.test_command))
        return 0

    print("Telegram runtime is not implemented yet. Use --test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
