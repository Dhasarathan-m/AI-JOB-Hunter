"""Service layer for orchestrating job scraping from multiple providers."""

from __future__ import annotations

import logging

from backend.database.job_repository import JobRepository
from backend.database.session import AsyncSessionLocal
from backend.models.job import Job
from backend.scraper.base import BaseScraper
from backend.scraper.remoteok_scraper import RemoteOkScraper

logger = logging.getLogger(__name__)


class ScraperService:
    """Coordinate scraping operations, duplicate handling, and persistence."""

    def __init__(self, scrapers: list[BaseScraper] | None = None) -> None:
        """Initialize the service with one or more scraper instances."""
        self._scrapers: list[BaseScraper] = scrapers or [RemoteOkScraper()]
        self._repository: JobRepository | None = None

    async def get_jobs(self) -> list[Job]:
        """Fetch jobs from all configured scrapers, save them, and return them."""
        all_jobs: list[Job] = []

        for scraper in self._scrapers:
            try:
                scraped_jobs = await scraper.scrape()
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.exception("Scraper %s failed: %s", scraper.__class__.__name__, exc)
                continue

            if not scraped_jobs:
                logger.info("Scraper %s returned no jobs", scraper.__class__.__name__)
                continue

            logger.info(
                "Scraper %s returned %d jobs",
                scraper.__class__.__name__,
                len(scraped_jobs),
            )
            all_jobs.extend(scraped_jobs)

        deduped_jobs = self._deduplicate_jobs(all_jobs)

        if not deduped_jobs:
            logger.info("No jobs were collected from the configured scrapers")
            return []

        try:
            async with AsyncSessionLocal() as session:
                self._repository = JobRepository(session)
                saved_count = await self._repository.save_jobs(deduped_jobs)
                logger.info("Persisted %d jobs through the repository", saved_count)
        except Exception as exc:
            logger.exception("Failed to persist scraped jobs: %s", exc)

        return deduped_jobs

    @staticmethod
    def _deduplicate_jobs(jobs: list[Job]) -> list[Job]:
        """Remove jobs that share the same company, title, and apply link."""
        seen: set[tuple[str, str, str]] = set()
        deduped: list[Job] = []

        for job in jobs:
            key = (
                job.company.lower().strip(),
                job.title.lower().strip(),
                job.apply_link.lower().strip(),
            )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(job)

        return deduped
