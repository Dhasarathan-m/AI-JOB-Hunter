"""Shared HTTP scraper foundation and common utilities."""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

from backend.models.job import Job

ScrapedJob = Job

logger = logging.getLogger(__name__)


class ScraperError(Exception):
    """Generic exception raised by scraper HTTP helpers."""


class BaseScraper(ABC):
    """Base class that manages HTTP requests, retries, and rate limiting."""

    source_name: str
    enabled: bool = True

    @property
    def default_headers(self) -> dict[str, str]:
        """Default headers used for every outgoing HTTP request."""
        return {
            "Accept": "application/json",
            "User-Agent": "AI Job Hunter Bot/1.0",
        }

    @property
    def timeout_seconds(self) -> float:
        """Timeout value for HTTP requests in seconds."""
        return 30.0

    @property
    def max_retries(self) -> int:
        """Maximum number of HTTP retry attempts."""
        return 3

    @property
    def backoff_factor(self) -> float:
        """Base multiplier for exponential backoff delays."""
        return 0.5

    @property
    def rate_limit_delay(self) -> float:
        """Delay between requests to avoid rate limiting."""
        return 0.5

    async def _sleep(self, seconds: float) -> None:
        """Sleep helper that can be mocked in tests."""
        await asyncio.sleep(seconds)

    async def _request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
    ) -> httpx.Response:
        """Execute an HTTP request with retry, backoff, and rate limiting."""
        resolved_headers = {**self.default_headers, **(headers or {})}
        attempt = 0

        while True:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout_seconds)) as client:
                    response = await client.request(
                        method,
                        url,
                        params=params,
                        headers=resolved_headers,
                        json=json,
                    )
                    response.raise_for_status()
                    return response
            except httpx.HTTPError as exc:
                if attempt >= self.max_retries:
                    logger.exception(
                        "%s request failed after %s attempts: %s %s",
                        getattr(self, "source_name", "scraper"),
                        attempt,
                        method,
                        url,
                    )
                    raise ScraperError(
                        f"{getattr(self, 'source_name', 'scraper')} request failed for {url}"
                    ) from exc

                delay = self.backoff_factor * 2 ** (attempt - 1)
                logger.warning(
                    "%s request attempt %s failed for %s: %s. Retrying in %.1f seconds",
                    getattr(self, "source_name", "scraper"),
                    attempt,
                    url,
                    exc,
                    delay,
                )
                await self._sleep(delay)
            else:
                await self._sleep(self.rate_limit_delay)

    async def fetch_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Fetch JSON data from the given URL."""
        response = await self._request("GET", url, params=params, headers=headers)
        try:
            return response.json()
        except ValueError as exc:
            logger.exception(
                "%s returned invalid JSON for %s",
                getattr(self, "source_name", "scraper"),
                url,
            )
            raise ScraperError(
                f"Invalid JSON response from {getattr(self, 'source_name', 'scraper')}"
            ) from exc

    @staticmethod
    def normalize_text(value: Any) -> str | None:
        """Normalize arbitrary values into trimmed strings."""
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None
        return str(value).strip() or None

    def create_job(
        self,
        title: str,
        company: str,
        apply_link: str,
        source: str | None = None,
        location: str | None = None,
        description: str | None = None,
        experience: str | None = None,
        salary: str | None = None,
        posted_date: str | None = None,
    ) -> Job:
        """Build a canonical Job model from raw values."""
        return Job(
            title=title,
            company=company,
            location=location or "",
            experience=experience,
            salary=salary,
            description=description,
            apply_link=apply_link,
            source=source or self.source_name,
            posted_date=posted_date,
        )

    @abstractmethod
    async def scrape(self) -> list[Job]:
        """Collect job listings from the external source."""
        raise NotImplementedError
