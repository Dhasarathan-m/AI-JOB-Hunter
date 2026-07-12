"""Factory that builds the list of active scrapers from target configuration."""

from backend.scraper.base import BaseScraper
from backend.scraper.career_page import CareerPageScraper
from backend.scraper.greenhouse import GreenhouseScraper
from backend.scraper.lever import LeverScraper
from backend.scraper.placeholders import (
    FounditScraper,
    IndeedScraper,
    LinkedInScraper,
    NaukriScraper,
    WellfoundScraper,
)
from backend.scraper.remoteok_scraper import RemoteOkScraper
from backend.scraper.rss import RssScraper
from backend.scraper.targets import (
    CAREER_PAGE_TARGETS,
    GREENHOUSE_TARGETS,
    LEVER_TARGETS,
    RSS_TARGETS,
)


def build_scrapers(include_playwright: bool = False) -> list[BaseScraper]:
    """Return all configured scrapers.

    Args:
        include_playwright: When False, skip browser-based scrapers (faster default).
    """
    scrapers: list[BaseScraper] = []

    scrapers.append(RemoteOkScraper())
    scrapers.extend(GreenhouseScraper(target) for target in GREENHOUSE_TARGETS)
    scrapers.extend(LeverScraper(target) for target in LEVER_TARGETS)
    scrapers.extend(RssScraper(target) for target in RSS_TARGETS)

    scrapers.extend(
        [LinkedInScraper(), IndeedScraper(), NaukriScraper(), FounditScraper(), WellfoundScraper()]
    )

    if include_playwright:
        scrapers.extend(CareerPageScraper(target) for target in CAREER_PAGE_TARGETS)

    return scrapers
