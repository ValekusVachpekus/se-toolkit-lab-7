"""LMS API client for the Telegram bot.

This module provides a client for interacting with the LMS backend API.
All requests use Bearer token authentication.
"""

from __future__ import annotations

import httpx


class LmsApiError(Exception):
    """Base exception for LMS API errors."""

    pass


class LmsConnectionError(LmsApiError):
    """Raised when the backend is unreachable."""

    pass


class LmsApiException(LmsApiError):
    """Raised when the API returns an error response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class LmsApiClient:
    """Client for the LMS backend API.

    Usage:
        client = LmsApiClient(base_url="http://localhost:42002", api_key="your-key")
        items = await client.get_items()
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10.0,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def _request(self, method: str, path: str, **kwargs) -> dict | list:
        """Make an API request with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., "/items/")
            **kwargs: Additional arguments for httpx

        Returns:
            Parsed JSON response

        Raises:
            LmsConnectionError: If the backend is unreachable
            LmsApiException: If the API returns an error
        """
        try:
            response = await self._client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            raise LmsConnectionError(f"connection refused ({self.base_url}). Check that the services are running.") from e
        except httpx.TimeoutException as e:
            raise LmsConnectionError(f"timeout connecting to {self.base_url}. The backend may be overloaded.") from e
        except httpx.HTTPStatusError as e:
            raise LmsApiException(
                status_code=e.response.status_code,
                message=e.response.text[:200] or f"{e.response.status_code} {e.response.reason_phrase}",
            ) from e

    async def get_items(self) -> list[dict]:
        """Get all items (labs and tasks) from the backend.

        Returns:
            List of item dictionaries
        """
        return await self._request("GET", "/items/")

    async def get_learners(self) -> list[dict]:
        """Get all enrolled learners.

        Returns:
            List of learner dictionaries
        """
        return await self._request("GET", "/learners/")

    async def get_analytics_scores(self, lab: str) -> dict:
        """Get score distribution for a lab.

        Args:
            lab: Lab identifier (e.g., "lab-04")

        Returns:
            Score distribution data
        """
        return await self._request("GET", "/analytics/scores", params={"lab": lab})

    async def get_pass_rates(self, lab: str) -> dict:
        """Get per-task pass rates for a lab.

        Args:
            lab: Lab identifier (e.g., "lab-04")

        Returns:
            Pass rates data with task names and percentages
        """
        return await self._request("GET", "/analytics/pass-rates", params={"lab": lab})

    async def get_timeline(self, lab: str) -> dict:
        """Get submission timeline for a lab.

        Args:
            lab: Lab identifier

        Returns:
            Timeline data
        """
        return await self._request("GET", "/analytics/timeline", params={"lab": lab})

    async def get_groups(self, lab: str) -> dict:
        """Get per-group performance for a lab.

        Args:
            lab: Lab identifier

        Returns:
            Group performance data
        """
        return await self._request("GET", "/analytics/groups", params={"lab": lab})

    async def get_top_learners(self, lab: str, limit: int = 5) -> dict:
        """Get top learners for a lab.

        Args:
            lab: Lab identifier
            limit: Number of top learners to return

        Returns:
            Top learners data
        """
        return await self._request("GET", "/analytics/top-learners", params={"lab": lab, "limit": limit})

    async def get_completion_rate(self, lab: str) -> dict:
        """Get completion rate for a lab.

        Args:
            lab: Lab identifier

        Returns:
            Completion rate data
        """
        return await self._request("GET", "/analytics/completion-rate", params={"lab": lab})

    async def trigger_sync(self) -> dict:
        """Trigger ETL data sync.

        Returns:
            Sync result data
        """
        return await self._request("POST", "/pipeline/sync", json={})
