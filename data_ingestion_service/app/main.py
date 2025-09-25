import asyncio
from data_ingestion_service.app.services.ingestion import IngestionService
from data_ingestion_service.app.core.logger import setup_logger

setup_logger()


async def main():
    """
    Application entrypoint.

    Initializes and run the ingestion service, which starts a Kafka consumer.
    """
    ingestion_service = IngestionService()
    await ingestion_service.run()


if __name__ == "__main__":
    asyncio.run(main())
