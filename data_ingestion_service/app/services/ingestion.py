from data_ingestion_service.app.consumers.kafka_consumer import ProductConsumer
from typing import Optional


class IngestionService:
    """
    Service responsible for orchestrating the data ingestion workflow.

    It initializes a Kafka consumer, which processes incoming messages.
    """

    def __init__(self, consumer: Optional[ProductConsumer] = None):
        self.consumer = consumer or ProductConsumer()

    async def run(self):
        try:
            await self.consumer.start()
            await self.consumer.consume()

        finally:
            await self.consumer.stop()
