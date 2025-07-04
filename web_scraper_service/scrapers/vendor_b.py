"""
Stub version of Vendor B scraper for story/demo purposes.

Provides a minimal implementation of a vendor-specific scraper for
testing and demonstration, without real scraping logic.
"""

from typing import Dict, Any
from .base_scraper import BaseScraper


class VendorBScraper(BaseScraper):
    """
    Stub implementation of Vendor B scraper.

    Returns hardcoded HTML and data, suitable for testing
    scraper integration and structure without real scraping logic.
    """

    def __init__(self, name: str = "vendor_b", **kwargs):
        """
        Initialize the stub Vendor B scraper.

        Args:
            name (str, optional): Name of the scraper (default: "vendor_b").
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
        return "<html><head><title>Vendor B Stub</title></head><body>Vendor B demo content</body></html>"

    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        """
        Return a stubbed dictionary representing parsed data.

        Args:
            html (str): HTML content to "parse" (ignored in stub).
            url (str): Source URL (included in result for completeness).

        Returns:
            Dict[str, Any]: Dummy structured data and metadata for Vendor B.
        """
        return {
            "url": url,
            "timestamp": 0,
            "data_points": {
                "title": "Vendor B Stub",
                "description": "Stub description for Vendor B",
                "content": {"text": "Demo content", "length": 12, "paragraphs": 1},
                "media": {
                    "images": [],
                    "videos": [],
                    "audio": [],
                    "counts": {"images": 0, "videos": 0, "audio": 0},
                },
                "vendor_specific_data": {
                    "service_info": None,
                    "pricing_tiers": None,
                    "user_reviews": None,
                    "ratings": None,
                },
            },
            "metadata": {
                "html_length": len(html),
                "scraper": self.name,
                "vendor": "vendor_b",
                "has_javascript": False,
                "has_forms": False,
                "has_tables": False,
                "has_video": False,
                "has_audio": False,
                "meta_tags_count": 0,
                "links_count": 0,
                "images_count": 0,
                "scripts_count": 0,
            },
        }
