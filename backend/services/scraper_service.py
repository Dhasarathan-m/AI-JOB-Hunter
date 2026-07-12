"""Service layer for orchestrating job scraping from multiple providers."""

from __future__ import annotations

import logging
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.job_repository import JobRepository
from backend.database.session import AsyncSessionLocal
from backend.models.job import Job
from backend.models.schemas import ScrapeRunResponse, ScrapeSourceResult
from backend.scraper.base import BaseScraper
from backend.scraper.manager import ScraperManager

logger = logging.getLogger(__name__)


class ScraperService:
    """Coordinate scraping operations, filtering, deduplication, and persistence."""

    def __init__(self, session: AsyncSession | None = None, scrapers: list[BaseScraper] | None = None) -> None:
        """Initialize the service with an optional session and a list of scrapers."""
        self._session = session
        self._scrapers = scrapers

    async def run_all(self, include_playwright: bool = False) -> ScrapeRunResponse:
        """Run configured scrapers, save new jobs, and return a scrape summary."""
        manager = ScraperManager(
            scrapers=self._scrapers,
            include_playwright=include_playwright,
        )
        scraped_jobs = await manager.run()
        total_found = len(scraped_jobs)
        deduped_jobs = self._deduplicate_jobs(scraped_jobs)
        total_filtered = total_found - len(deduped_jobs)
        total_created = 0
        total_skipped = 0
        results: list[ScrapeSourceResult] = []

        async with self._get_session() as session:
            repository = JobRepository(session)

            if deduped_jobs:
                total_created = await repository.save_jobs(deduped_jobs)
                total_skipped = len(deduped_jobs) - total_created

        logger.info("Persisted %d jobs through the repository", total_created)

        return ScrapeRunResponse(
            total_found=total_found,
            total_created=total_created,
            total_skipped=total_skipped,
            total_filtered=total_filtered,
            results=results,
        )

    @staticmethod
    def _deduplicate_jobs(jobs: Iterable[Job]) -> list[Job]:
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

    async def _get_session(self) -> AsyncSession:
        """Return the configured session or create a new session."""
        if self._session is not None:
            return self._session

        return AsyncSessionLocal()

    @staticmethod
    def _extract_company(scraper: BaseScraper) -> str:
        """Extract the scraper's configured company name when available."""
        target = getattr(scraper, "_target", None)
        if target is None:
            return "unknown"
        company = getattr(target, "company", None)
        return str(company) if company is not None else "unknown"
