from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    bot_token: str | None = None
    lms_api_base_url: str = "http://localhost:42002"
    lms_api_key: str = ""
    llm_api_key: str = ""
    llm_api_base_url: str = "http://localhost:42005/v1"
    llm_api_model: str = "qwen3-coder-flash"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env.bot.secret"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

