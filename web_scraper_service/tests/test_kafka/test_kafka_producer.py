"""Kafka producer module for sending scraped data to Kafka topics.

Handles Kafka client configuration, message serialization, and
publishing data to relevant topics in the ingestion pipeline.
"""

import logging
import anyio
from aiokafka import AIOKafkaProducer
from typing import Any
from web_scraper_service.app.core.config import settings

logger = logging.getLogger("kafka_producer")


class KafkaProducerService:
    """Asynchronous Kafka producer service for publishing product data.

    This service initializes a Kafka producer client, serializes product data,
    sends messages with retry logic, and logs results.
    """

    def __init__(self):
        """Initializes the KafkaProducerService using global settings.

        Sets up broker addresses, topic name, and max retries from app settings.
        """
        self.brokers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = settings.KAFKA_TOPIC
        self.max_retries = settings.KAFKA_MAX_RETRIES
        self._producer = None

    async def start(self) -> None:
        """Initializes and starts the Kafka producer.

        Raises:
            Exception: If the producer cannot be started.
        """
        self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
        await self._producer.start()
        logger.info("Kafka producer started for topic: %s", self.topic)

    async def stop(self) -> None:
        """Stops the Kafka producer gracefully.

        Returns:
            None
        """
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")

    async def send_product(self, product_model: Any) -> None:
        """Serializes and sends product data to Kafka with retries.

        Args:
            product_model (Any): Product data as a Pydantic model or dict.

        Raises:
            RuntimeError: If the producer is not started.
            ValueError: If product_model cannot be serialized.
        """
        if not self._producer:
            raise RuntimeError("Kafka producer is not started. Call start() first.")

        message_bytes = self._serialize(product_model)
        attempt = 0

        while attempt < self.max_retries:
            try:
                await self._producer.send_and_wait(self.topic, message_bytes)
                logger.info(
                    "Message sent to Kafka topic '%s' on attempt %d",
                    self.topic,
                    attempt + 1,
                )
                return
            except Exception as e:
                logger.error("Kafka send attempt %d failed: %s", attempt + 1, str(e))
                attempt += 1
                await anyio.sleep(2)
        logger.error("All retries failed. Message was not sent to Kafka.")

    @staticmethod
    def _serialize(product_model: Any) -> bytes:
        """Serializes product data into JSON-encoded bytes.

        Args:
            product_model (Any): The product data to serialize (Pydantic model or dict).

        Returns:
            bytes: The JSON-encoded product data.

        Raises:
            ValueError: If the input cannot be serialized to JSON.
        """
        if hasattr(product_model, "model_dump_json"):
            return product_model.model_dump_json().encode("utf-8")
        elif isinstance(product_model, dict):
            import json

            return json.dumps(product_model).encode("utf-8")
        else:
            raise ValueError(
                "Cannot serialize product_model: must be a Pydantic model or dict."
            )
