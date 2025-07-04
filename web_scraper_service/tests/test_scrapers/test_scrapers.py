"""
Pytest suite for web scraper modules.

Tests scraper instantiation, factory functions, and custom exceptions.
"""

import pytest
from scrapers import (
    VendorAScraper,
    VendorBScraper,
    ScrapingException,
    get_available_scrapers,
    create_scraper,
)


def test_vendor_a_instantiation():
    scraper_default = VendorAScraper()
    assert scraper_default.name == "vendor_a"

    scraper_custom = VendorAScraper(name="custom_a")
    assert scraper_custom.name == "custom_a"


def test_vendor_a_stub_methods():
    scraper = VendorAScraper()
    html = scraper.fetch_html("http://fake-url.com")
    parsed_data = scraper.parse_html(html, "http://fake-url.com")

    assert "Stub content" in html
    assert parsed_data["data_points"]["title"] == "Stub Title"
    assert parsed_data["metadata"]["vendor"] == "vendor_a"


def test_vendor_b_instantiation():
    scraper_default = VendorBScraper()
    assert scraper_default.name == "vendor_b"

    scraper_custom = VendorBScraper(name="custom_b")
    assert scraper_custom.name == "custom_b"


def test_vendor_b_stub_methods():
    scraper = VendorBScraper()
    html = scraper.fetch_html("http://fake-url.com")
    parsed_data = scraper.parse_html(html, "http://fake-url.com")

    assert "Vendor B demo content" in html
    assert parsed_data["data_points"]["title"] == "Vendor B Stub"
    assert parsed_data["metadata"]["vendor"] == "vendor_b"


@pytest.mark.parametrize("scraper_name", get_available_scrapers())
def test_factory_creates_scrapers(scraper_name):
    scraper = create_scraper(scraper_name)
    assert scraper.name == scraper_name
    assert isinstance(scraper, (VendorAScraper, VendorBScraper))


def test_scraping_exception():
    error_message = "A stub error occurred"
    with pytest.raises(ScrapingException, match=error_message) as exc_info:
        raise ScrapingException(error_message)

    assert str(exc_info.value) == error_message
