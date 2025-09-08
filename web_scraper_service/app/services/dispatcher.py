# web_scraper_service/app/services/dispatcher.py
import logging
from typing import Optional, Dict, Type

from web_scraper_service.app.services.kafka_producer import KafkaProducerService

# --- IMPORT ALL YOUR PYDANTIC MODELS ---
from web_scraper_service.app.models.products.base_products import BaseProduct
from web_scraper_service.app.models.products.laptop import Laptop
from web_scraper_service.app.models.products.desktop import Desktop
from web_scraper_service.app.models.products.monitor import Monitor
# ... import other models as you create them (Tablet, Mouse, etc.)

logger = logging.getLogger("dispatcher")

# --- CREATE A MAPPING FROM CATEGORY NAME TO PYDANTIC MODEL CLASS ---
PRODUCT_MODEL_MAP: Dict[str, Type[BaseProduct]] = {
    "laptops": Laptop,
    "desktops": Desktop,
    "monitors": Monitor,
    # Add other mappings here as you create scrapers for them
}


class MockScraper:
    # ... (rest of the mock scraper is the same)
    def parse_html(self, html: str, url: str) -> dict:
        return {
            "product_type": "laptop",  # <-- Add product_type to mock data
            "product_name": "Mock Product",
            "model": "M-123",
            "brand": "MockBrand",
            "sku": "MOCK123",
            "price": 42.0,
            "availability": "in_stock",
            "url": "http://example.com/mock",
        }


def create_scraper(scraper_name: str) -> MockScraper:
    return MockScraper()


class ScraperDispatcher:
    """Coordinates scraping, validation, and data publishing workflows."""

    def __init__(self, kafka_producer: Optional[KafkaProducerService] = None):
        self.kafka_producer = kafka_producer or KafkaProducerService()

    async def process_product_scraping(
        self,
        scraper_name: str,
        url: str,
        category: str,  # <-- Add category
    ) -> None:
        """Orchestrates scraping, validation, and Kafka publishing."""
        try:
            # --- THIS LOGIC IS REFACTORED ---
            ProductModel = PRODUCT_MODEL_MAP.get(category)
            if not ProductModel:
                logger.error("No Pydantic model found for category: %s", category)
                return

            await self.kafka_producer.start()
            scraper = create_scraper(scraper_name)
            html = scraper.fetch_html(url)
            parsed_data = scraper.parse_html(html, url)

            # This line now validates the data against the correct model for the category
            product = ProductModel(**parsed_data)

            await self.kafka_producer.send_product(product)
            logger.info(
                "Product from %s sent to Kafka topic 'products-%s'.",
                url,
                product.product_type,
            )
        except Exception as e:
            logger.error("Failed to process scraping for %s: %s", url, str(e))
        finally:
            if self.kafka_producer._producer:
                await self.kafka_producer.stop()
