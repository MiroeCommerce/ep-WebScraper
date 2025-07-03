"""
Stub version of Vendor A scraper for story/demo purposes.
"""

from typing import Dict, Any
from .base_scraper import BaseScraper


class VendorAScraper(BaseScraper):
    """Stub implementation of Vendor A scraper."""

    def __init__(self, name: str = "vendor_a", **kwargs):
        super().__init__(name, **kwargs)

    def fetch_html(self, url: str) -> str:
        # Stubbed HTML response
        return "<html><head><title>Stub Title</title></head><body>Stub content</body></html>"

    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        # Stubbed parsed data
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
