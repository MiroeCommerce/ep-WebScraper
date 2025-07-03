"""
Stub test suite for web scraper modules.

Minimal tests for VendorAScraper, VendorBScraper, factory, and exception.

Belongs to: Web Scraper Service - Tests
"""

import unittest
from scrapers import (
    VendorAScraper,
    VendorBScraper,
    ScrapingException,
    get_available_scrapers,
    create_scraper,
)


class TestVendorAScraperStub(unittest.TestCase):
    def test_basic_instantiation(self):
        scraper = VendorAScraper("vendor_a_stub")
        self.assertEqual(scraper.name, "vendor_a_stub")


class TestVendorBScraperStub(unittest.TestCase):
    def test_basic_instantiation(self):
        scraper = VendorBScraper("vendor_b_stub")
        self.assertEqual(scraper.name, "vendor_b_stub")


class TestFactoryStub(unittest.TestCase):
    def test_factory_creates_scrapers(self):
        available = get_available_scrapers()
        for name in available:
            scraper = create_scraper(name)
            self.assertEqual(scraper.name, name)


class TestScrapingExceptionStub(unittest.TestCase):
    def test_scraping_exception_message(self):
        msg = "stub error"
        e = ScrapingException(msg)
        self.assertEqual(str(e), msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
