import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pytest
from unittest.mock import AsyncMock
from data_ingestion_service.app.services.ingestion import IngestionService
from data_ingestion_service.app.consumers.kafka_consumer import ProductConsumer

@pytest.mark.asyncio
async def test_ingestion_service_run_calls_methods():
    mock_consumer = AsyncMock(spec=ProductConsumer)

    mock_consumer.consume.return_value = None

    service = IngestionService(consumer=mock_consumer)

    await service.run()

    mock_consumer.start.assert_awaited_once()
    mock_consumer.consume.assert_awaited_once()
    mock_consumer.stop.assert_awaited_once()