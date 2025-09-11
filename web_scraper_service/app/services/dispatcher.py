# Mocking the dispatcher file. To be resolved further
import logging
from typing import Optional, Dict, Type

from web_scraper_service.app.services.kafka_producer import KafkaProducerService
from web_scraper_service.app.scrapers import create_scraper
from web_scraper_service.app.models.products.base_products import BaseProduct
from web_scraper_service.app.models.products.laptop import Laptop
from web_scraper_service.app.models.products.desktop import Desktop
from web_scraper_service.app.models.products.monitor import Monitor

logger = logging.getLogger("dispatcher")

PRODUCT_MODEL_MAP: Dict[str, Type[BaseProduct]] = {
    "laptops": Laptop,
    "desktops": Desktop,
    "monitors": Monitor,
}


class ScraperDispatcher:
    """Coordinates scraping, validation, and data publishing workflows."""

    def __init__(self, kafka_producer: Optional[KafkaProducerService] = None):
        self.kafka_producer = kafka_producer or KafkaProducerService()

    async def process_product_scraping(
        self, scraper_name: str, url: str, category: str
    ) -> None:
        """Orchestrates scraping, validation, and Kafka publishing."""
        try:
            ProductModel = PRODUCT_MODEL_MAP.get(category)
            if not ProductModel:
                logger.error("No Pydantic model found for category: %s", category)
                return

            await self.kafka_producer.start()
            scraper = create_scraper(scraper_name)
            html = scraper.fetch_html(url)
            parsed_data = scraper.parse_html(html, url)

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
            # FIX: Check for the _producer attribute on the kafka_producer instance
            if self.kafka_producer and self.kafka_producer._producer:
                await self.kafka_producer.stop()
