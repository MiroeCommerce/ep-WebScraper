"""Dispatcher module to orchestrate scraper execution.

This module handles routing requests to the appropriate scraper implementations,
manages the scraper lifecycle (fetching and parsing), error handling, and
publishing validated product data to Kafka.
"""

import logging
import anyio
from typing import Optional

from web_scraper_service.app.services.kafka_producer import KafkaProducerService
from web_scraper_service.app.models.product import LaptopProduct

logger = logging.getLogger("dispatcher")


class MockScraper:
    """A mock scraper used for testing the dispatcher pipeline."""

    def fetch_html(self, url: str) -> str:
        """Fetches HTML from the given URL.

        Args:
            url (str): The URL to fetch HTML from.

        Returns:
            str: The HTML content as a string.
        """
        return "<html><body>Mock HTML for {}</body></html>".format(url)

    def parse_html(self, html: str, url: str) -> dict:
        """Parses HTML and extracts product data.

        Args:
            html (str): The HTML content to parse.
            url (str): The URL from which the HTML was fetched.

        Returns:
            dict: The parsed product data.
        """
        return {
            "name": "Mock Product",
            "sku": "MOCK123",
            "price": 42.0,
            "vendor": "MockVendor",
            "url": url,
            "available": True,
            "ram": "16GB",
            "cpu": "Intel i7",
            "screen_size": "15.6 inch",
            "storage": "512GB SSD",
        }


def create_scraper(scraper_name: str) -> MockScraper:
    """Creates a scraper instance by name.

    Args:
        scraper_name (str): The name of the scraper to create.

    Returns:
        MockScraper: An instance of the requested scraper.
    """
    return MockScraper()


class ScraperDispatcher:
    """Coordinates scraping, validation, and data publishing workflows."""

    def __init__(self, kafka_producer: Optional[KafkaProducerService] = None):
        """Initializes the ScraperDispatcher.

        Args:
            kafka_producer (Optional[KafkaProducerService]): An instance of the
                Kafka producer. If not provided, a new one will be created.
                This allows for dependency injection during testing.
        """
        self.kafka_producer = kafka_producer or KafkaProducerService()

    async def process_product_scraping(self, scraper_name: str, url: str) -> None:
        """Orchestrates scraping, validation, and Kafka publishing.

        Args:
            scraper_name (str): The name of the scraper to use.
            url (str): The product URL to scrape.

        Returns:
            None
        """
        try:
            await self.kafka_producer.start()
            scraper = create_scraper(scraper_name)
            html = scraper.fetch_html(url)
            parsed_data = scraper.parse_html(html, url)
            product = LaptopProduct(**parsed_data)
            await self.kafka_producer.send_product(product)
            logger.info("Product from %s sent to Kafka.", url)
        except Exception as e:
            logger.error("Failed to process scraping for %s: %s", url, str(e))
        finally:
            await self.kafka_producer.stop()

    async def mock_run(self) -> None:
        """Runs a demo/test entrypoint with mocked data.

        This method demonstrates the scraping and publishing workflow
        using mock data and a mock scraper.
        """
        test_scraper = "vendor_a"
        test_url = "http://mocked-url.com/product/123"
        await self.process_product_scraping(test_scraper, test_url)


if __name__ == "__main__":
    dispatcher = ScraperDispatcher()
    anyio.run(dispatcher.mock_run())
