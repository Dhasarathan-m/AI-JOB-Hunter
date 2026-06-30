"""Shared types and base class for all job scrapers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ScrapedJob:
    """Normalized job data produced by any scraper before database storage."""

    title: str
    company: str
    url: str
    source: str
    location: str | None = None
    description: str | None = None


class BaseScraper(ABC):
    """Contract every scraper must follow (Open/Closed Principle)."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Short identifier stored in the jobs.source column."""

    @abstractmethod
    async def scrape(self) -> list[ScrapedJob]:
        """Collect job listings from the external source."""
