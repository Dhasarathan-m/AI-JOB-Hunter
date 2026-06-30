"""Orchestrates scrapers and persists results through JobService."""

import logging

from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.schemas import JobCreate, ScrapeRunResponse, ScrapeSourceResult
from backend.scraper.base import BaseScraper, ScrapedJob
from backend.scraper.filters import is_cybersecurity_job
from backend.scraper.registry import build_scrapers
from backend.services.job_service import JobService

logger = logging.getLogger(__name__)


class ScraperService:
    """Runs configured scrapers and stores new cybersecurity jobs."""

    def __init__(self, session: AsyncSession) -> None:
        self._job_service = JobService(session)

    async def run_all(self, include_playwright: bool = False) -> ScrapeRunResponse:
        """Execute every configured scraper and persist matching jobs."""
        scrapers = build_scrapers(include_playwright=include_playwright)
        results: list[ScrapeSourceResult] = []

        for scraper in scrapers:
            result = await self._run_scraper(scraper)
            results.append(result)

        return ScrapeRunResponse(
            total_found=sum(item.jobs_found for item in results),
            total_created=sum(item.jobs_created for item in results),
            total_skipped=sum(item.jobs_skipped for item in results),
            total_filtered=sum(item.jobs_filtered for item in results),
            results=results,
        )

    async def _run_scraper(self, scraper: BaseScraper) -> ScrapeSourceResult:
        """Run one scraper and track created, skipped, and filtered counts."""
        company = self._resolve_company(scraper)

        try:
            scraped_jobs = await scraper.scrape()
        except Exception as exc:
            logger.exception("Scraper failed: %s (%s)", scraper.source_name, company)
            return ScrapeSourceResult(
                source=scraper.source_name,
                company=company,
                jobs_found=0,
                jobs_created=0,
                jobs_skipped=0,
                jobs_filtered=0,
                error=str(exc),
            )

        created = 0
        skipped = 0
        filtered = 0

        for scraped in scraped_jobs:
            if settings.scrape_filter_cybersecurity_only and not is_cybersecurity_job(
                scraped.title,
                scraped.description,
            ):
                filtered += 1
                continue

            job_create = self._to_job_create(scraped)
            stored = await self._job_service.create_job_if_new(job_create)
            if stored:
                created += 1
            else:
                skipped += 1

        return ScrapeSourceResult(
            source=scraper.source_name,
            company=company,
            jobs_found=len(scraped_jobs),
            jobs_created=created,
            jobs_skipped=skipped,
            jobs_filtered=filtered,
        )

    @staticmethod
    def _resolve_company(scraper: BaseScraper) -> str:
        """Read company name from scraper target when available."""
        target = getattr(scraper, "_target", None)
        return getattr(target, "company", scraper.source_name)

    @staticmethod
    def _to_job_create(scraped: ScrapedJob) -> JobCreate:
        """Convert a scraped job into a validated API/database payload."""
        location = scraped.location
        if location and len(location) > 255:
            location = location[:252] + "..."

        return JobCreate(
            title=scraped.title,
            company=scraped.company,
            url=HttpUrl(scraped.url),
            source=scraped.source,
            location=location,
            description=scraped.description,
        )
