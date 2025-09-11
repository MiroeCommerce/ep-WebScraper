"""Kafka producer for sending scraped product data.

This module provides the KafkaProducerService, a class responsible for
connecting to Kafka, serializing Pydantic product models, and publishing them
to dynamic, type-specific topics (e.g., 'products-laptop'). It includes
asynchronous handling and a retry mechanism for robust message delivery.
"""

import anyio
import json
from aiokafka import AIOKafkaProducer
from typing import Any, Optional
from web_scraper_service.app.core.config import settings
from web_scraper_service.app.utils.loguru_logger import logger


class KafkaProducerService:
    """Asynchronous Kafka producer service for publishing product data.

    This service manages the lifecycle of an AIOKafkaProducer, handles the
    serialization of product data models, and sends messages to Kafka topics
    that are dynamically determined by the product's type.

    Attributes:
        brokers (str): Comma-separated list of Kafka bootstrap servers.
        max_retries (int): The maximum number of times to retry sending a
            message upon failure.
        _producer (Optional[AIOKafkaProducer]): The underlying aiokafka producer
            instance, initialized on start().
    """

    def __init__(self):
        """Initializes the KafkaProducerService with settings."""
        self.brokers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.max_retries = settings.KAFKA_MAX_RETRIES
        self._producer: Optional[AIOKafkaProducer] = None

    async def start(self) -> None:
        """Initializes and starts the underlying Kafka producer client.

        Connects to the Kafka brokers specified in the application settings.
        This method is idempotent; it will not create a new producer if one
        is already running.
        """
        if not self._producer:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()
            logger.info("Kafka producer started.")

    async def stop(self) -> None:
        """Stops the Kafka producer client gracefully.

        This method is idempotent and safe to call even if the producer is
        already stopped.
        """
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")
            self._producer = None

    async def send_product(self, product_model: Any) -> None:
        """Serializes and sends a product model to a type-specific Kafka topic.

        This method determines the target topic from the model's `product_type`
        attribute (e.g., a model with `product_type='laptop'` is sent to the
        'products-laptop' topic). It attempts to send the message with a
        configured number of retries.

        Args:
            product_model (Any): The Pydantic product model to be sent. Must
                contain a `product_type` attribute.

        Raises:
            RuntimeError: If the producer has not been started via `start()`.
            ValueError: If the `product_model` does not have a `product_type`
                attribute.
        """
        if not self._producer:
            raise RuntimeError("Kafka producer is not started. Call start() first.")

        if not hasattr(product_model, "product_type"):
            raise ValueError("Product model must have a 'product_type' attribute.")

        topic = f"products-{product_model.product_type}"
        message_bytes = self._serialize(product_model)
        attempt = 0

        while attempt < self.max_retries:
            try:
                await self._producer.send_and_wait(topic, message_bytes)
                logger.info(
                    "Message sent to Kafka topic '%s' on attempt %d",
                    topic,
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
        """Serializes the product data into a JSON-encoded bytes object.

        Args:
            product_model (Any): The product data to serialize (Pydantic model
                or dict).

        Returns:
            bytes: The JSON-encoded product data.

        Raises:
            ValueError: If `product_model` is not a Pydantic model or a dict
                and cannot be serialized.
        """
        if hasattr(product_model, "model_dump_json"):
            return product_model.model_dump_json().encode("utf-8")
        elif isinstance(product_model, dict):
            return json.dumps(product_model).encode("utf-8")
        else:
            raise ValueError(
                "Cannot serialize product_model: must be a Pydantic model or dict."
            )
