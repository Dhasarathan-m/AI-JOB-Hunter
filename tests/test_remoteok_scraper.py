import unittest
from unittest import mock

from backend.scraper.remoteok_scraper import RemoteOkScraper


class RemoteOkScraperTests(unittest.IsolatedAsyncioTestCase):
    async def test_scrape_returns_jobs_on_valid_payload(self):
        sample_payload = [
            {
                "position": "Security Engineer",
                "company": "ExampleCo",
                "location": "Remote",
                "apply_url": "https://example.com/apply",
                "description": "Test job",
            }
        ]

        scraper = RemoteOkScraper()
        with mock.patch.object(scraper, "fetch_json", return_value=sample_payload):
            jobs = await scraper.scrape()

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "Security Engineer")
        self.assertEqual(jobs[0].company, "ExampleCo")
        self.assertEqual(jobs[0].apply_link, "https://example.com/apply")

    async def test_scrape_returns_empty_on_invalid_payload(self):
        scraper = RemoteOkScraper()
        with mock.patch.object(scraper, "fetch_json", return_value={"error": "nope"}):
            jobs = await scraper.scrape()

        self.assertEqual(jobs, [])
