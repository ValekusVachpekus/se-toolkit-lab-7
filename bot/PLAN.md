# Development Plan — LMS Telegram Bot

## Overview

This document outlines the development plan for building a Telegram bot that provides access to the LMS (Learning Management System) backend. The bot will support slash commands for structured interactions and natural language queries powered by an LLM for flexible user experiences.

## Architecture Summary

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point** (`bot.py`) — Handles Telegram bot startup and CLI test mode
2. **Handlers** (`handlers/`) — Command logic as pure functions (no Telegram dependency)
3. **Services** (`services/`) — External API clients (LMS backend, LLM provider)
4. **Configuration** (`config.py`) — Environment variable loading with validation

This architecture enables **testable handlers**: the same handler functions work in `--test` mode, unit tests, and production Telegram runtime.

## Task 1: Scaffold and Test Mode

**Goal:** Establish project structure with offline test capability.

- Create `bot/` directory with `pyproject.toml` for dependency management
- Implement `--test` mode in entry point for CLI-based command testing
- Build handler module with placeholder responses for all P0 commands
- Document architecture and testing approach

**Why this first:** Test mode allows development without Telegram API access, enabling rapid iteration and CI integration.

## Task 2: Backend Integration

**Goal:** Connect handlers to the real LMS backend API.

- Create `services/lms_api.py` client with Bearer token authentication
- Implement `/health` handler with actual backend connectivity check
- Implement `/labs` handler to fetch available labs from `GET /items`
- Implement `/scores <lab>` handler to fetch analytics from `GET /analytics`
- Add error handling for network failures and API errors
- Update handlers to use dependency injection for testability

**Key pattern:** API client encapsulates HTTP details; handlers focus on response formatting.

## Task 3: Intent-Based Natural Language Routing

**Goal:** Enable plain language queries via LLM tool use.

- Create `services/llm_client.py` for LLM API interactions
- Wrap all 9 backend endpoints as LLM tools with clear descriptions
- Build intent router that lets LLM decide which tool to call based on user input
- Implement tool execution and response formatting
- Add conversation context for multi-turn interactions (optional)

**Critical insight:** Tool description quality determines routing accuracy more than prompt engineering. If the LLM picks the wrong tool, improve the description — don't add regex fallbacks.

## Task 4: Containerization and Deployment

**Goal:** Deploy bot alongside backend on the VM.

- Create `Dockerfile` for the bot service
- Add bot to `docker-compose.yml` with proper networking
- Configure environment variables for production (`.env.docker.secret`)
- Document deployment process and troubleshooting steps
- Set up health checks and logging

**Docker networking note:** Containers communicate via service names (e.g., `backend`), not `localhost`.

## Testing Strategy

- **Unit tests:** Handler functions with mocked services
- **Integration tests:** Full command flow with test backend
- **CLI test mode:** `--test` flag for manual verification without Telegram
- **Production verification:** Deploy to VM and test in real Telegram

## Git Workflow

Each task follows the standard workflow:

1. Create GitHub issue for the task
2. Create feature branch (`feature/task-N-description`)
3. Implement with frequent commits
4. Open PR referencing issue (`Closes #N`)
5. Partner review and merge

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| LLM picks wrong tool | Invest in clear tool descriptions; test with varied inputs |
| Backend API changes | Abstract behind service layer; update one client module |
| Bot token exposure | Use `.env.bot.secret` (gitignored); never commit secrets |
| Docker networking issues | Use service names; test connectivity before deployment |

## Success Criteria

By the end of this development plan:

- ✅ All P0 commands work in test mode and Telegram
- ✅ Backend integration returns real data
- ✅ Natural language queries route correctly via LLM
- ✅ Bot deployed and running on VM
- ✅ Documentation enables future maintenance
