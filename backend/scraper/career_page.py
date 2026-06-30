"""Playwright scraper for custom company career pages without public APIs."""

import logging

from playwright.async_api import Page

from backend.scraper.base import ScrapedJob
from backend.scraper.playwright_base import PlaywrightScraper, soup
from backend.scraper.targets import CareerPageTarget

logger = logging.getLogger(__name__)


class CareerPageScraper(PlaywrightScraper):
    """Scrape job links from a career page using CSS selectors.

    Use this when a company does not expose Greenhouse/Lever JSON APIs
    but still publishes listings on an HTML careers page.
    """

    source_name = "career_page"

    def __init__(self, target: CareerPageTarget) -> None:
        self._target = target

    async def _navigate(self, page: Page) -> None:
        """Load the career page and wait for network activity to settle."""
        logger.info("Loading career page: %s", self._target.url)
        await page.goto(self._target.url, wait_until="networkidle", timeout=60_000)

    async def parse_jobs(self, page: Page, html: str) -> list[ScrapedJob]:
        """Extract job titles and links matching the configured selector."""
        document = soup(html)
        links = document.select(self._target.job_link_selector)

        jobs: list[ScrapedJob] = []
        seen_urls: set[str] = set()

        for link in links:
            href = link.get("href", "").strip()
            title = link.get_text(strip=True)
            if not href or not title:
                continue

            url = href if href.startswith("http") else page.url.rstrip("/") + "/" + href.lstrip("/")
            if url in seen_urls:
                continue

            seen_urls.add(url)
            jobs.append(
                ScrapedJob(
                    title=title,
                    company=self._target.company,
                    url=url,
                    source=self.source_name,
                )
            )

        logger.info(
            "Career page %s: found %d job links",
            self._target.company,
            len(jobs),
        )
        return jobs
