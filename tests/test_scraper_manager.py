import unittest
from unittest import mock

from backend.models.job import Job
from backend.scraper.manager import ScraperManager


class DummyScraper:
    def __init__(self, name: str, jobs: list[Job], enabled: bool = True):
        self.source_name = name
        self.enabled = enabled
        self.called = False
        self._jobs = jobs

    async def scrape(self):
        self.called = True
        return self._jobs


class ScraperManagerTests(unittest.IsolatedAsyncioTestCase):
    async def test_run_returns_combined_jobs(self):
        jobs_a = [Job(title="A", company="Co", location="Remote", apply_link="1", source="a")]
        jobs_b = [Job(title="B", company="Co", location="Remote", apply_link="2", source="b")]
        manager = ScraperManager(scrapers=[DummyScraper("a", jobs_a), DummyScraper("b", jobs_b)])

        combined_jobs = await manager.run()

        self.assertEqual(len(combined_jobs), 2)
        self.assertEqual(combined_jobs[0].title, "A")
        self.assertEqual(combined_jobs[1].title, "B")

    async def test_run_skips_disabled_scrapers(self):
        jobs = [Job(title="A", company="Co", location="Remote", apply_link="1", source="a")]
        manager = ScraperManager(scrapers=[DummyScraper("a", jobs, enabled=False)])

        combined_jobs = await manager.run()

        self.assertEqual(combined_jobs, [])

    async def test_run_continues_if_scraper_fails(self):
        class FailingScraper(DummyScraper):
            async def scrape(self):
                raise RuntimeError("boom")

        jobs = [Job(title="A", company="Co", location="Remote", apply_link="1", source="a")]
        manager = ScraperManager(scrapers=[FailingScraper("fail", []), DummyScraper("success", jobs)])

        combined_jobs = await manager.run()

        self.assertEqual(len(combined_jobs), 1)
