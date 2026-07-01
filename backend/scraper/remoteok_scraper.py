"""RemoteOK scraper implementation for fetching public job listings."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from backend.models.job import Job
from backend.scraper.base import BaseScraper

logger = logging.getLogger(__name__)

REMOTEOK_API_URL = "https://remoteok.com/api"


class RemoteOkScraper(BaseScraper):
    """Fetch and normalize job listings from the RemoteOK public API."""

    source_name = "remoteok"

    async def scrape(self) -> list[Job]:
        """Fetch jobs from RemoteOK and return them as Job models."""
        logger.info("Fetching RemoteOK jobs from %s", REMOTEOK_API_URL)

        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(
                    REMOTEOK_API_URL,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            logger.error("RemoteOK request failed: %s", exc)
            return []
        except ValueError as exc:
            logger.error("RemoteOK response was not valid JSON: %s", exc)
            return []

        if not isinstance(payload, list):
            logger.warning("Unexpected RemoteOK payload type: %s", type(payload).__name__)
            return []

        jobs: list[Job] = []
        for item in payload:
            job = self._to_job_model(item)
            if job is not None:
                jobs.append(job)

        logger.info("RemoteOK scrape completed successfully: %d jobs parsed", len(jobs))
        return jobs

    def _to_job_model(self, item: Any) -> Job | None:
        """Convert a RemoteOK payload item into a validated Job model."""
        if not isinstance(item, dict):
            return None

        title = self._clean_text(item.get("position") or item.get("title"))
        company = self._clean_text(item.get("company") or item.get("company_name"))
        location = self._clean_text(item.get("location") or item.get("location_text"))
        description = self._clean_text(item.get("description") or item.get("description_text"))
        apply_link = self._clean_text(
            item.get("apply_url")
            or item.get("url")
            or item.get("link")
            or item.get("job_url")
        )
        salary = self._clean_text(item.get("salary"))
        experience = self._clean_text(item.get("experience"))
        posted_date = self._clean_text(item.get("date") or item.get("created_at"))

        if not title or not company or not apply_link:
            logger.debug("Skipping RemoteOK item without essential fields: %s", item)
            return None

        return Job(
            title=title,
            company=company,
            location=location or "Remote",
            experience=experience,
            salary=salary,
            description=description,
            apply_link=apply_link,
            source=self.source_name,
            posted_date=posted_date,
        )

    @staticmethod
    def _clean_text(value: Any) -> str | None:
        """Normalize string-like values from the API payload."""
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None
        return str(value).strip() or None
