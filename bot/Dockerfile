# LMS Telegram Bot Dockerfile
# Uses uv for dependency management (no requirements.txt)

FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy bot source code
COPY bot/ ./bot/

# Set working directory to bot
WORKDIR /app/bot

# Run the bot
CMD ["uv", "run", "bot.py"]
