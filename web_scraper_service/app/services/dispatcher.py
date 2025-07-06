"""Dispatcher module to orchestrate scraper execution.

Handles routing requests to appropriate scraper implementations,
manages scraper lifecycle (fetch, parse), error handling,
and publishing validated product data to Kafka.

Use the scraper registry to dynamically select scraper classes.
"""

import logging
import anyio

from app.services.kafka_producer import KafkaProducerService
from app.models.product import LaptopProduct  # Using LaptopProduct as an example

logger = logging.getLogger("dispatcher")


class MockScraper:
    """A mock scraper used for testing the dispatcher pipeline."""

    def fetch_html(self, url: str) -> str:
        """Returns mock HTML content for a given URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: Mocked HTML content.
        """
        return "<html><body>Mock HTML for {}</body></html>".format(url)

    def parse_html(self, html: str, url: str) -> dict:
        """Parses HTML and returns mocked product data.

        Args:
            html (str): HTML content to parse.
            url (str): The original URL.

        Returns:
            dict: Parsed product data compatible with LaptopProduct.
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
    """Factory to create a scraper instance by name.

    Args:
        scraper_name (str): The name of the scraper.

    Returns:
        MockScraper: The mock scraper instance (stub).
    """
    return MockScraper()


class ScraperDispatcher:
    """Coordinates scraping, validation, and data publishing workflows."""

    def __init__(self):
        """Initializes the ScraperDispatcher with a Kafka producer."""
        self.kafka_producer = KafkaProducerService()

    async def process_product_scraping(self, scraper_name: str, url: str) -> None:
        """Orchestrates scraping, validation, and Kafka publishing.

        Args:
            scraper_name (str): Name of the scraper class to use.
            url (str): URL to scrape.

        Raises:
            Exception: If any step in the pipeline fails.
        """
        try:
            # 1. Start the Kafka producer (should ideally be done once globally)
            await self.kafka_producer.start()

            # 2. Instantiate the scraper by name
            scraper = create_scraper(scraper_name)

            # 3. Fetch and parse product data (mocked or real)
            html = scraper.fetch_html(url)
            parsed = scraper.parse_html(html, url)

            # 4. Validate product with a Pydantic model
            product = LaptopProduct(**parsed)  # Switch model as needed

            # 5. Send Kafka
            await self.kafka_producer.send_product(product)

            logger.info("Product from %s sent to Kafka.", url)
        except Exception as e:
            logger.error("Failed to process scraping for %s: %s", url, str(e))
            # Optionally handle errors, retries, dead letter queue, etc.
        finally:
            await self.kafka_producer.stop()  # For test/demo, stop after each

    async def mock_run(self) -> None:
        """Demo/test entrypoint with mocked data.

        This method runs the full pipeline with a mock scraper and test URL.
        """
        test_scraper = "vendor_a"
        test_url = "http://mocked-url.com/product/123"
        await self.process_product_scraping(test_scraper, test_url)


if __name__ == "__main__":
    dispatcher = ScraperDispatcher()
    anyio.run(dispatcher.mock_run())
