import json
import re
from typing import Dict, Optional, Type, Any

import asyncio
from aiokafka import AIOKafkaConsumer

from data_ingestion_service.app.core.config import settings
from data_ingestion_service.app.core.logger import logger
from data_ingestion_service.app.schemas.products import (
    Desktop,
    Keyboard,
    Laptop,
    Monitor,
    Mouse,
    Processor,
    Tablet,
)

from data_ingestion_service.app.core.database import Database
from data_ingestion_service.app.crud import ProductCRUD, CategoryCRUD


PRODUCT_TYPE: Dict[str, Type[Any]] = {
    "desktop": Desktop,
    "laptop": Laptop,
    "monitor": Monitor,
    "mouse": Mouse,
    "keyboard": Keyboard,
    "processor": Processor,
    "tablet": Tablet,
}


class ProductConsumer:
    """
    Kafka consumer responsible for ingesting product data.

    The consumer listens to product-related topics published by the
    web scraper service, validates the incoming messages against
    Pydantic models, and persists valid product data into PostgreSQL
    using SQLAlchemy.
    """

    def __init__(self):
        self.topic_prefix = settings.KAFKA_TOPIC_PREFIX
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.group_id = settings.KAFKA_CONSUMER_GROUP
        self._consumer: Optional[AIOKafkaConsumer] = None
        self.db = Database()

    async def start(self):
        """
        Start the Kafka consumer and subscribe to product topics.

        Subscribes to all topics matching the prefix defined in settings,
        initializes the consumer, and logs the subscription details.
        """
        self._consumer = AIOKafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )
        pattern = re.compile(rf"{self.topic_prefix}-.*")
        self._consumer.subscribe(pattern=pattern)
        await self._consumer.start()
        subscribed = self._consumer.subscription()
        logger.info(f"Kafka Consumer started for topics {list(subscribed)}")

    async def stop(self):
        """
        Stop the Kafka consumer gracefully.

        Ensures the consumer shuts down cleanly and logs the shutdown event.
        """
        if self._consumer:
            await self._consumer.stop()

            logger.info("Kafka Consumer stopped.")

    async def save_product_with_retries(
        self,
        product_crud: ProductCRUD,
        category_crud: CategoryCRUD,
        product: Any,
        max_attempts: int = 3,
    ):
        """
        Persist product data to the database with retry logic.

        Args:
            product_crud (ProductCRUD): CRUD handler for product persistence.
            category_crud (CategoryCRUD): CRUD handler for category persistence.
            product (Any): Validated product data (Pydantic model).
            max_attempts (int): Maximum retry attempts in case of failure.

        Raises:
            Exception: Reraises the last exception if all retry attempts fail.
        """
        attempt = 0
        while attempt <= max_attempts:
            try:
                await category_crud.get_or_create_category(product.product_type)
                result = await product_crud.process_product(product_data=product)

                if result == "created":
                    logger.info(
                        f"Product {product.product_name} was added to the database."
                    )
                elif result == "updated":
                    logger.info(f"Product {product.product_name} was updated.")
                return
            except Exception as e:
                attempt += 1
                logger.warning(
                    f"Attempt {attempt} failed for product {product.product_name}: {e}"
                )
                if attempt >= max_attempts:
                    raise

    async def process_message(self, msg: bytes, topic: str):
        """
        Process a single Kafka message.

        - Determines the product type from the topic.
        - Validates the incoming message with the appropriate Pydantic model.
        - Persists the product data to the database.

        Args:
            msg (bytes): The Kafka message payload.
            topic (str): The topic name the message was consumed from.

        Logs:
            - Warnings if no Pydantic model exists for the topic.
            - Errors if validation or persistence fails.
        """
        product_name = topic.replace(f"{self.topic_prefix}-", "")
        product_model = PRODUCT_TYPE.get(product_name)
        if product_model is None:
            logger.warning(f"No Pydantic model for topic {topic}.")
            return

        try:
            message_data = json.loads(msg.decode("utf-8"))
            product = product_model(**message_data)

            async with self.db.session_scope() as session:
                product_crud = ProductCRUD(session)
                category_crud = CategoryCRUD(session)

                await self.save_product_with_retries(
                    product_crud=product_crud,
                    category_crud=category_crud,
                    product=product,
                )
                logger.info(f"Product {product.product_name} saved to database.")

        except Exception as e:
            logger.error(f"Validation failed for topic: {topic}, error: {e}")
            return

    async def consume(self, commit_interval: int = 10):
        """
        Main consumption loop for Kafka messages.

        Continuously consumes messages, processes them, and commits
        offsets in batches to ensure reliability.

        Args:
            commit_interval (int): Number of successfully processed
                messages before committing offsets.

        Raises:
            RuntimeError: If the consumer has not been started.

        Logs:
            - Errors during message processing.
            - Cancellation or shutdown events.
        """
        if not self._consumer:
            raise RuntimeError("Kafka consumer not started.")
        processed_count = 0
        try:
            async for msg in self._consumer:
                success = False
                try:
                    await self.process_message(msg.value, msg.topic)
                    success = True
                except Exception as e:
                    logger.error(
                        f"Error processing message from topic: {msg.topic}, error: {e}"
                    )
                if success:
                    processed_count += 1

                if processed_count >= commit_interval:
                    await self._consumer.commit()
                    processed_count = 0

        except asyncio.CancelledError:
            logger.info("Kafka consumer loop cancelled.")
        finally:
            await self.stop()
