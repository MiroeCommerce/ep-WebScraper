"""
Stub version of Vendor A scraper for story/demo purposes.

Provides a minimal implementation of a vendor-specific scraper for
testing and demonstration, without real scraping logic.
"""

from typing import Dict, Any
from .base_scraper import BaseScraper


class VendorAScraper(BaseScraper):
    """
    Stub implementation of Vendor A scraper.

    Provides fixed HTML and parsed data for demonstration and unit testing.
    """

    def __init__(self, name: str = "vendor_a", **kwargs):
        """
        Initialize the stub Vendor A scraper.

        Args:
            name (str, optional): Name of the scraper (default: "vendor_a").
            **kwargs: Additional arguments (not used in stub).
        """
        super().__init__(name, **kwargs)

    def fetch_html(self, url: str) -> str:
        """
        Return a stubbed HTML string as a fake response.

        Args:
            url (str): The URL to "fetch" (ignored in stub).

        Returns:
            str: Fixed HTML string for demo/testing purposes.
        """
        return "<html><head><title>Stub Title</title></head><body>Stub content</body></html>"

    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        """
        Return a stubbed dictionary representing parsed data.

        Args:
            html (str): HTML content to "parse" (ignored in stub).
            url (str): Source URL (included in result for completeness).

        Returns:
            Dict[str, Any]: Dummy structured data and metadata.
        """
        return {
            "url": url,
            "timestamp": 0,
            "data_points": {
                "title": "Stub Title",
                "description": "Stub Description",
                "images": [],
                "links": [],
                "vendor_specific_data": {
                    "product_info": None,
                    "pricing": None,
                    "availability": None,
                },
            },
            "metadata": {
                "html_length": len(html),
                "scraper": self.name,
                "vendor": "vendor_a",
                "has_javascript": False,
                "has_forms": False,
                "has_tables": False,
                "meta_tags_count": 0,
                "links_count": 0,
                "images_count": 0,
            },
        }
