import asyncio
import unittest
from unittest import mock

import httpx

from backend.scraper.base import BaseScraper, ScraperError


class TestBaseScraper(BaseScraper):
    source_name = "test"

    async def scrape(self):
        return []


class BaseScraperTests(unittest.IsolatedAsyncioTestCase):
    async def test_normalize_text(self):
        self.assertEqual(BaseScraper.normalize_text(" text "), "text")
        self.assertEqual(BaseScraper.normalize_text(123), "123")
        self.assertIsNone(BaseScraper.normalize_text(None))
        self.assertIsNone(BaseScraper.normalize_text("   "))

    async def test_request_retries_and_success(self):
        scraper = TestBaseScraper()
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"ok": True}

        async def fake_request(*args, **kwargs):
            if fake_request.call_count == 0:
                fake_request.call_count += 1
                raise httpx.HTTPError("temporary")
            return response

        fake_request.call_count = 0

        fake_client = mock.AsyncMock()
        fake_client.__aenter__.return_value = fake_client
        fake_client.request.side_effect = fake_request

        with mock.patch("backend.scraper.base.httpx.AsyncClient", return_value=fake_client):
            result = await scraper.fetch_json("https://example.com")

        self.assertEqual(result, {"ok": True})
        self.assertGreaterEqual(fake_request.call_count, 1)

    async def test_request_raises_scraper_error_after_retries(self):
        scraper = TestBaseScraper()

        fake_client = mock.AsyncMock()
        fake_client.__aenter__.return_value = fake_client
        fake_client.request.side_effect = httpx.HTTPError("fatal")

        with mock.patch("backend.scraper.base.httpx.AsyncClient", return_value=fake_client):
            with self.assertRaises(ScraperError):
                await scraper.fetch_json("https://example.com")
