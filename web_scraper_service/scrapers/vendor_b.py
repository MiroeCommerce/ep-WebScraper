"""
Stub version of Vendor B scraper for story/demo purposes.
"""

from typing import Dict, Any
from .base_scraper import BaseScraper


class VendorBScraper(BaseScraper):
    """Stub implementation of Vendor B scraper."""

    def __init__(self, name: str = "vendor_b", **kwargs):
        super().__init__(name, **kwargs)

    def fetch_html(self, url: str) -> str:
        # Stubbed HTML content
        return "<html><head><title>Vendor B Stub</title></head><body>Vendor B demo content</body></html>"

    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        # Stubbed data output
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
