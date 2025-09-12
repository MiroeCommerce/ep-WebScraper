import json
import re
from typing import Dict, Optional

import anyio
from aiokafka import AIOKafkaConsumer

from data_ingestion_service.app.core.config import settings
from data_ingestion_service.app.core.logger import logger, setup_logger
from data_ingestion_service.app.schemas.products import (
    Desktop,
    Keyboard,
    Laptop,
    Monitor,
    Mouse,
    Processor,
    Tablet,
)

# Need to include the SQLAlchemy models
PRODUCT_TYPE: Dict[str, tuple] = {
    "products-desktop": Desktop,
    "products-laptop": Laptop,
    "products-monitor": Monitor,
    "products-mouse": Mouse,
    "products-keyboard": Keyboard,
    "products-processor": Processor,
    "prodcuts-table": Tablet,
}

# May need to move the setup_logger to main.py
setup_logger()


class ProductConsumer:
    def __init__(self, topic: Optional[str] = None):
        self.topic_prefix = settings.KAFKA_TOPIC_PREFIX
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.group_id = settings.KAFKA_CONSUMER_GROUP
        self._consumer = Optional[AIOKafkaConsumer] = None

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        pattern = re.compile(rf"{self.topic_prefix}-.*")
        self._consumer.subscribe(pattern=pattern)
        await self._consumer.start()
        logger.info(f"Kafka Consumer started for topic {self.topic}")

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()

            logger.info("Kafka Consumer stopped.")

    async def process_message(self, msg: bytes, topic: str):
        product_model = PRODUCT_TYPE.get(topic)
        if product_model is None:
            logger.warning(f"No Pydantic model for topic {topic}.")

        try:
            message_data = json.loads(msg.decode("utf-8"))
            product = product_model(**message_data)
            # TODO - include the save to db, possibly from a crud.py

        except Exception as e:
            logger.error(f"Validation failed for topic: {topic}, error: {e}")
            return

    async def consume(self):
        # if not self._consumer:
        #     raise RuntimeError('Kafka consumer not started.')
        try:
            async for msg in self._consumer:
                try:
                    await self.process_message(msg.value, msg.topic)
                    await self._consumer.commit()
                except Exception as e:
                    logger.error(
                        f"Error processing message from topic: {msg.topic}, error: {e}"
                    )
        except anyio.CancelledError:
            logger.info("Kafka consumer loop cancelled.")
        finally:
            await self.stop()
