"""
Test package for the scrapers' module.

Stub test loader for minimal validation of scrapers and factory.

Belongs to: Web Scraper Service - Tests - Scrapers
"""

from .test_scrapers import (
    TestVendorAScraperStub,
    TestVendorBScraperStub,
    TestFactoryStub,
    TestScrapingExceptionStub,
)

__all__ = [
    "TestVendorAScraperStub",
    "TestVendorBScraperStub",
    "TestFactoryStub",
    "TestScrapingExceptionStub",
]
