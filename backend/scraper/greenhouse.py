"""Greenhouse job board scraper using the public JSON API."""

import logging

import httpx

from backend.scraper.base import BaseScraper, ScrapedJob
from backend.scraper.targets import GreenhouseTarget

logger = logging.getLogger(__name__)

GREENHOUSE_API_URL = "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"


class GreenhouseScraper(BaseScraper):
    """Fetch jobs from Greenhouse boards via their documented public API.

    Why API instead of Playwright here?
    - Faster and more reliable (no browser overhead)
    - Greenhouse exposes structured JSON intentionally
    - Playwright is reserved for sites without APIs (see career_page.py)
    """

    source_name = "greenhouse"

    def __init__(self, target: GreenhouseTarget) -> None:
        self._target = target

    async def scrape(self) -> list[ScrapedJob]:
        """Download and normalize all jobs for the configured board."""
        url = GREENHOUSE_API_URL.format(board_token=self._target.board_token)
        logger.info("Fetching Greenhouse board: %s", self._target.board_token)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params={"content": "true"})
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            logger.error(
                "Greenhouse request failed for %s: %s",
                self._target.board_token,
                exc,
            )
            raise

        jobs: list[ScrapedJob] = []
        for item in payload.get("jobs", []):
            location_data = item.get("location") or {}
            jobs.append(
                ScrapedJob(
                    title=item.get("title", "").strip(),
                    company=self._target.company,
                    url=item.get("absolute_url", "").strip(),
                    source=self.source_name,
                    location=location_data.get("name"),
                    description=item.get("content"),
                )
            )

        logger.info(
            "Greenhouse %s: found %d jobs",
            self._target.company,
            len(jobs),
        )
        return jobs
