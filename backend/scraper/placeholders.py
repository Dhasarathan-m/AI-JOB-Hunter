"""Placeholder scraper implementations for future job source integrations."""

from __future__ import annotations

import logging

from backend.models.job import Job
from backend.scraper.base import BaseScraper

logger = logging.getLogger(__name__)


class LinkedInScraper(BaseScraper):
    """Placeholder for a LinkedIn scraper implementation."""

    source_name = "linkedin"
    enabled = False

    async def scrape(self) -> list[Job]:
        """Placeholder scraper; implementation will be added later."""
        logger.info("LinkedIn scraper is currently disabled")
        return []


class IndeedScraper(BaseScraper):
    """Placeholder for an Indeed scraper implementation."""

    source_name = "indeed"
    enabled = False

    async def scrape(self) -> list[Job]:
        """Placeholder scraper; implementation will be added later."""
        logger.info("Indeed scraper is currently disabled")
        return []


class NaukriScraper(BaseScraper):
    """Placeholder for a Naukri scraper implementation."""

    source_name = "naukri"
    enabled = False

    async def scrape(self) -> list[Job]:
        """Placeholder scraper; implementation will be added later."""
        logger.info("Naukri scraper is currently disabled")
        return []


class FounditScraper(BaseScraper):
    """Placeholder for a Foundit scraper implementation."""

    source_name = "foundit"
    enabled = False

    async def scrape(self) -> list[Job]:
        """Placeholder scraper; implementation will be added later."""
        logger.info("Foundit scraper is currently disabled")
        return []


class WellfoundScraper(BaseScraper):
    """Placeholder for a Wellfound scraper implementation."""

    source_name = "wellfound"
    enabled = False

    async def scrape(self) -> list[Job]:
        """Placeholder scraper; implementation will be added later."""
        logger.info("Wellfound scraper is currently disabled")
        return []
