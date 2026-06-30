"""Scraper target definitions for cybersecurity job sources."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GreenhouseTarget:
    """Greenhouse board configuration."""

    board_token: str
    company: str


@dataclass(frozen=True)
class LeverTarget:
    """Lever company board configuration."""

    slug: str
    company: str


@dataclass(frozen=True)
class RssTarget:
    """RSS feed configuration."""

    url: str
    company: str


@dataclass(frozen=True)
class CareerPageTarget:
    """Custom career page that requires a browser (Playwright)."""

    url: str
    company: str
    job_link_selector: str = "a[href*='jobs'], a[href*='careers']"


# Cybersecurity-focused companies using public Greenhouse boards.
# Verify board tokens at: https://boards.greenhouse.io/{token}
GREENHOUSE_TARGETS: list[GreenhouseTarget] = [
    GreenhouseTarget(board_token="cloudflare", company="Cloudflare"),
    GreenhouseTarget(board_token="datadog", company="Datadog"),
]

LEVER_TARGETS: list[LeverTarget] = [
    # Add Lever slugs here after verifying at: https://jobs.lever.co/{slug}
]

RSS_TARGETS: list[RssTarget] = [
    # Add RSS feeds here — many job boards deprecated RSS in recent years.
]

# Fallback for pages without a public JSON API (Playwright + BeautifulSoup).
CAREER_PAGE_TARGETS: list[CareerPageTarget] = [
    CareerPageTarget(
        url="https://boards.greenhouse.io/cloudflare",
        company="Cloudflare",
        job_link_selector="a[href*='/jobs/']",
    ),
]

# Keywords used to keep only security-relevant listings.
CYBERSECURITY_KEYWORDS: tuple[str, ...] = (
    "security",
    "cyber",
    "soc",
    "infosec",
    "threat",
    "vulnerability",
    "penetration",
    "forensic",
    "incident",
    "grc",
    "devsecops",
    "malware",
    "identity",
    "iam",
    "ciso",
    "red team",
    "blue team",
    "appsec",
    "zero trust",
)
