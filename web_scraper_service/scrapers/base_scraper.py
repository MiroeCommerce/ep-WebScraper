"""
Base scraper stub for demonstration purposes.

Defines the interface and minimal logic for all vendor-specific scrapers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers.

    Provides a minimal interface for vendor-specific scrapers, including
    method signatures for fetching and parsing HTML, as well as batch scraping.

    Args:
        name (str): Unique name or type of the scraper.
        timeout (int, optional): Timeout for page loads or requests (default: 20).
        headless (bool, optional): Whether to run the scraper in headless mode (default: True).
    """

    def __init__(self, name: str, timeout: int = 20, headless: bool = True):
        self.name = name
        self.timeout = timeout
        self.headless = headless
        self.driver = None
        self.logger = None

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """
        Fetch raw HTML from the given URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: HTML content as a string.

        Raises:
            ScrapingException: If fetching fails (to be implemented in subclasses).
        """
        pass

    @abstractmethod
    def parse_html(self, html: str, url: str) -> Dict[str, Any]:
        """
        Parse the fetched HTML and extract structured data.

        Args:
            html (str): HTML content as a string.
            url (str): The source URL (for metadata/context).

        Returns:
            Dict[str, Any]: Structured data extracted from the HTML.

        Raises:
            ScrapingException: If parsing fails (to be implemented in subclasses).
        """
        pass

    def scrape(
        self, url: str, save_html: bool = True, output_folder: str = "./scraped_pages"
    ) -> Dict[str, Any]:
        """
        Run a complete scrape for a single URL.

        Args:
            url (str): URL to scrape.
            save_html (bool, optional): Whether to save HTML to disk (default: True).
            output_folder (str, optional): Folder to save HTML files (default: "./scraped_pages").

        Returns:
            Dict[str, Any]: Scrape result with metadata and (dummy) data.
        """
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
        """
        Run the scrape method for multiple URLs.

        Args:
            urls (List[str]): List of URLs to scrape.
            save_html (bool, optional): Whether to save HTML to disk (default: True).
            output_folder (str, optional): Folder to save HTML files (default: "./scraped_pages").

        Returns:
            List[Dict[str, Any]]: List of scrape results.
        """
        return [self.scrape(url, save_html, output_folder) for url in urls]

    def __enter__(self) -> "BaseScraper":
        """
        Context manager entry. Used for resource management in subclasses.

        Returns:
            BaseScraper: self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit. Used for cleanup in subclasses.

        Args:
            exc_type: Exception type (if any).
            exc_val: Exception value (if any).
            exc_tb: Traceback object (if any).
        """
        pass


class ScrapingException(Exception):
    """
    Custom exception for scraping-related errors.

    Raised by scraper implementations when fetching or parsing fails.
    """

    pass
