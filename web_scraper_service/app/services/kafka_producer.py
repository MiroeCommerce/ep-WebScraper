# web_scraper_service/app/services/kafka_producer.py

import anyio
import json
from aiokafka import AIOKafkaProducer
from typing import Any, Optional
from web_scraper_service.app.core.config import settings
from web_scraper_service.app.utils.loguru_logger import logger


class KafkaProducerService:
    """Asynchronous Kafka producer service for publishing product data."""

    def __init__(self):  # <--- REMOVED topic from __init__
        """Initializes the KafkaProducerService."""
        self.brokers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.max_retries = settings.KAFKA_MAX_RETRIES
        self._producer: Optional[AIOKafkaProducer] = None

    async def start(self) -> None:
        """Initializes and starts the Kafka producer client."""
        if not self._producer:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()
            logger.info("Kafka producer started.")  # <--- Simplified log message

    async def stop(self) -> None:
        """Stops the Kafka producer client gracefully."""
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")
            self._producer = None

    async def send_product(self, product_model: Any) -> None:
        """Serializes and sends product data to a type-specific Kafka topic."""
        if not self._producer:
            raise RuntimeError("Kafka producer is not started. Call start() first.")

        # --- THIS IS THE NEW LOGIC ---
        if not hasattr(product_model, "product_type"):
            raise ValueError("Product model must have a 'product_type' attribute.")

        topic = f"products-{product_model.product_type}"
        # --- END OF NEW LOGIC ---

        message_bytes = self._serialize(product_model)
        attempt = 0

        while attempt < self.max_retries:
            try:
                await self._producer.send_and_wait(
                    topic, message_bytes
                )  # <--- Use the dynamic topic
                logger.info(
                    "Message sent to Kafka topic '%s' on attempt %d",
                    topic,  # <--- Use the dynamic topic in the log
                    attempt + 1,
                )
                return
            except Exception as e:
                logger.error(
                    "Kafka send attempt %d to topic '%s' failed: %s",
                    attempt + 1,
                    topic,
                    str(e),
                )
                attempt += 1
                await anyio.sleep(2)
        logger.error("All retries failed. Message was not sent to topic '%s'.", topic)

    @staticmethod
    def _serialize(product_model: Any) -> bytes:
        """Serializes the product data into a JSON-encoded bytes object."""
        if hasattr(product_model, "model_dump_json"):
            return product_model.model_dump_json().encode("utf-8")
        elif isinstance(product_model, dict):
            return json.dumps(product_model).encode("utf-8")
        else:
            raise ValueError(
                "Cannot serialize product_model: must be a Pydantic model or dict."
            )
