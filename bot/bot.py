"""LMS Telegram Bot — Entry point.

Supports:
- CLI test mode: uv run bot.py --test "message"
- Telegram bot runtime (aiogram)
- Intent-based natural language routing via LLM
"""

from __future__ import annotations

import argparse
import logging

from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
    route_intent,
)
from config import BotSettings

# Inline keyboard buttons for common actions
INLINE_KEYBOARD_BUTTONS = [
    [{"text": "📚 Available Labs", "callback_data": "labs"}, {"text": "🏥 Health Check", "callback_data": "health"}],
    [{"text": "📊 Scores lab-04", "callback_data": "scores_lab-04"}, {"text": "📊 Scores lab-01", "callback_data": "scores_lab-01"}],
    [{"text": "❓ Help", "callback_data": "help"}],
]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


async def run_telegram_bot() -> None:
    """Run the Telegram bot with aiogram."""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command, CommandStart
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    settings = BotSettings()
    
    if not settings.bot_token:
        logger.error("BOT_TOKEN is not set. Cannot start Telegram bot.")
        return
    
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    logger.info("Telegram bot started. Polling for messages...")
    
    # Handler for /start
    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        response = handle_start()
        # Add inline keyboard
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📚 Available Labs", callback_data="labs"),
                 InlineKeyboardButton(text="🏥 Health Check", callback_data="health")],
                [InlineKeyboardButton(text="📊 Scores lab-04", callback_data="scores_lab-04"),
                 InlineKeyboardButton(text="📊 Scores lab-01", callback_data="scores_lab-01")],
                [InlineKeyboardButton(text="❓ Help", callback_data="help")],
            ]
        )
        await message.answer(response, reply_markup=keyboard)
    
    # Handler for /help
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        response = handle_help()
        await message.answer(response)
    
    # Handler for /health
    @dp.message(Command("health"))
    async def cmd_health(message: types.Message):
        response = handle_health()
        await message.answer(response)
    
    # Handler for /labs
    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message):
        response = handle_labs()
        await message.answer(response)
    
    # Handler for /scores
    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message):
        lab_id = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        response = handle_scores(lab_id)
        await message.answer(response)
    
    # Handler for callback queries (inline buttons)
    @dp.callback_query()
    async def process_callback(callback: types.CallbackQuery):
        await callback.answer()
        
        if callback.data == "labs":
            response = handle_labs()
        elif callback.data == "health":
            response = handle_health()
        elif callback.data == "help":
            response = handle_help()
        elif callback.data.startswith("scores_"):
            lab_id = callback.data.replace("scores_", "")
            response = handle_scores(lab_id)
        else:
            response = "Unknown action."
        
        await callback.message.answer(response)
    
    # Handler for plain text messages (LLM routing)
    @dp.message()
    async def handle_text(message: types.Message):
        if message.text:
            logger.info(f"Received message: {message.text[:50]}...")
            response = route_intent(message.text)
            await message.answer(response)
    
    # Start polling
    await dp.start_polling(bot)


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

    # Telegram runtime
    import asyncio
    asyncio.run(run_telegram_bot())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
