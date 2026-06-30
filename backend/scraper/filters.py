"""Keyword filter for security-related job titles."""

from backend.scraper.targets import CYBERSECURITY_KEYWORDS


def is_cybersecurity_job(title: str, description: str | None = None) -> bool:
    """Return True when the job title matches security keywords.

    We intentionally match on title only. Full descriptions from Greenhouse
    often mention 'security' even for non-security roles at security companies.
    """
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in CYBERSECURITY_KEYWORDS)
