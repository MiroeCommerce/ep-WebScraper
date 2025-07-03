"""
Base scraper stub for demonstration purposes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseScraper(ABC):
    def __init__(self, name: str, timeout: int = 20, headless: bool = True):
        self.name = name
        self.timeout = timeout
        self.headless = headless
        self.driver = None
        self.logger = None

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        pass

    @abstractmethod
    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        pass

    def scrape(
        self, url: str, save_html: bool = True, output_folder: str = "./scraped_pages"
    ) -> Dict[str, Any]:
        return {
            "url": url,
            "scraper": self.name,
            "success": True,
            "data": {},
            "error": None,
            "html_file": None,
        }

    def scrape_multiple(
        self,
        urls: List[str],
        save_html: bool = True,
        output_folder: str = "./scraped_pages",
    ) -> List[Dict[str, Any]]:
        return [self.scrape(url, save_html, output_folder) for url in urls]

    def __enter__(self) -> "BaseScraper":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


class ScrapingException(Exception):
    """Custom exception for scraping-related errors."""

    pass
