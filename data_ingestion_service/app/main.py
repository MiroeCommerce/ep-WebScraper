import asyncio
from data_ingestion_service.app.services.ingestion import IngestionService

async def main():
    ingestion_service = IngestionService()
    await ingestion_service.run()


if __name__ == '__main__':
    asyncio.run(main())