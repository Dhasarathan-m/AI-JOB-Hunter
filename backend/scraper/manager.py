"""Coordinator that executes scraper instances and aggregates results."""

from __future__ import annotations

import logging
from typing import Iterable, List

from backend.models.job import Job
from backend.scraper.base import BaseScraper
from backend.scraper.registry import build_scrapers

logger = logging.getLogger(__name__)


class ScraperManager:
    """Run configured scrapers and aggregate job results."""

    def __init__(
        self,
        scrapers: list[BaseScraper] | None = None,
        include_playwright: bool = False,
    ) -> None:
        """Initialize the scraper manager with a list of scraper instances."""
        self._scrapers = scrapers or build_scrapers(include_playwright=include_playwright)

    async def run(self) -> list[Job]:
        """Execute all enabled scrapers and return combined job results."""
        jobs: list[Job] = []
        for scraper in self._scrapers:
            if not getattr(scraper, "enabled", True):
                logger.info("Skipping disabled scraper: %s", scraper.__class__.__name__)
                continue

            try:
                source_jobs = await scraper.scrape()
            except Exception as exc:
                logger.exception("Scraper %s failed and will be skipped", scraper.__class__.__name__)
                continue

            if source_jobs:
                logger.info(
                    "Scraper %s returned %s jobs",
                    scraper.__class__.__name__,
                    len(source_jobs),
                )
                jobs.extend(source_jobs)
            else:
                logger.info("Scraper %s returned no jobs", scraper.__class__.__name__)

        return jobs

    def register(self, scraper: BaseScraper) -> None:
        """Register an additional scraper for future runs."""
        self._scrapers.append(scraper)

    def get_scrapers(self) -> list[BaseScraper]:
        """Return the current list of registered scrapers."""
        return list(self._scrapers)
