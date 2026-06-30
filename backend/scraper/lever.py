"""Lever job board scraper using the public JSON API."""

import logging

import httpx

from backend.scraper.base import BaseScraper, ScrapedJob
from backend.scraper.targets import LeverTarget

logger = logging.getLogger(__name__)

LEVER_API_URL = "https://api.lever.co/v0/postings/{slug}"


class LeverScraper(BaseScraper):
    """Fetch jobs from Lever boards via their public postings API."""

    source_name = "lever"

    def __init__(self, target: LeverTarget) -> None:
        self._target = target

    async def scrape(self) -> list[ScrapedJob]:
        """Download and normalize all jobs for the configured Lever company."""
        url = LEVER_API_URL.format(slug=self._target.slug)
        logger.info("Fetching Lever board: %s", self._target.slug)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params={"mode": "json"})
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            logger.error("Lever request failed for %s: %s", self._target.slug, exc)
            raise

        if not isinstance(payload, list):
            logger.warning("Unexpected Lever response for %s", self._target.slug)
            return []

        jobs: list[ScrapedJob] = []
        for item in payload:
            categories = item.get("categories") or {}
            jobs.append(
                ScrapedJob(
                    title=item.get("text", "").strip(),
                    company=self._target.company,
                    url=item.get("hostedUrl", "").strip(),
                    source=self.source_name,
                    location=categories.get("location"),
                    description=item.get("descriptionPlain"),
                )
            )

        logger.info("Lever %s: found %d jobs", self._target.company, len(jobs))
        return jobs
