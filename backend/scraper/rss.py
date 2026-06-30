"""RSS feed job scraper."""

import asyncio
import logging

import feedparser

from backend.scraper.base import BaseScraper, ScrapedJob
from backend.scraper.targets import RssTarget

logger = logging.getLogger(__name__)


class RssScraper(BaseScraper):
    """Parse job listings from RSS/Atom feeds.

    feedparser is synchronous, so we run it in a thread pool to avoid
    blocking FastAPI's async event loop.
    """

    source_name = "rss"

    def __init__(self, target: RssTarget) -> None:
        self._target = target

    async def scrape(self) -> list[ScrapedJob]:
        """Parse the configured RSS feed and return normalized jobs."""
        logger.info("Fetching RSS feed: %s", self._target.url)

        feed = await asyncio.to_thread(feedparser.parse, self._target.url)

        if feed.bozo:
            logger.warning(
                "RSS feed parse warning for %s: %s",
                self._target.url,
                feed.bozo_exception,
            )

        jobs: list[ScrapedJob] = []
        for entry in feed.entries:
            link = getattr(entry, "link", "").strip()
            title = getattr(entry, "title", "").strip()
            if not link or not title:
                continue

            description = getattr(entry, "summary", None)
            jobs.append(
                ScrapedJob(
                    title=title,
                    company=self._target.company,
                    url=link,
                    source=self.source_name,
                    description=description,
                )
            )

        logger.info("RSS %s: found %d entries", self._target.company, len(jobs))
        return jobs
