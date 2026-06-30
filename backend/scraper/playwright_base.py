"""Playwright-based scraper foundation for JavaScript-heavy career pages."""

import logging
from abc import abstractmethod

from bs4 import BeautifulSoup
from playwright.async_api import Browser, Page, async_playwright

from backend.scraper.base import BaseScraper, ScrapedJob

logger = logging.getLogger(__name__)


class PlaywrightScraper(BaseScraper):
    """Base class that manages browser lifecycle for HTML-based scrapers.

    Playwright launches a real Chromium browser, executes JavaScript, and
    returns fully rendered HTML — required for SPAs and dynamic career sites.

    Subclasses implement parse_jobs() to extract listings from page HTML.
    """

    @abstractmethod
    async def parse_jobs(self, page: Page, html: str) -> list[ScrapedJob]:
        """Extract job listings from rendered page content."""

    async def scrape(self) -> list[ScrapedJob]:
        """Launch browser, load page, delegate parsing to subclass."""
        async with async_playwright() as playwright:
            browser = await self._launch_browser(playwright.chromium)
            try:
                page = await browser.new_page()
                return await self._scrape_with_page(page)
            finally:
                await browser.close()

    async def _launch_browser(self, chromium) -> Browser:
        """Launch headless Chromium with sensible defaults."""
        return await chromium.launch(headless=True)

    async def _scrape_with_page(self, page: Page) -> list[ScrapedJob]:
        """Navigate to target URL and parse the rendered HTML."""
        await self._navigate(page)
        html = await page.content()
        return await self.parse_jobs(page, html)

    @abstractmethod
    async def _navigate(self, page: Page) -> None:
        """Open the target career page and wait for content to load."""


def soup(html: str) -> BeautifulSoup:
    """Parse HTML with BeautifulSoup (shared helper for Playwright scrapers)."""
    return BeautifulSoup(html, "html.parser")
