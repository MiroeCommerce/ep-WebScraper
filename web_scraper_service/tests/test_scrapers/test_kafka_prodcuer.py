# web_scraper_service/tests/test_scrapers/test_kafka_producer.py

import pytest
from unittest.mock import AsyncMock, patch

from app.models.product import LaptopProduct
from app.services.kafka_producer import KafkaProducerService

# A sample product to use across tests
SAMPLE_LAPTOP = LaptopProduct(
    name="Test Laptop",
    sku="TEST-SKU-123",
    price=1299.99,
    vendor="TestVendor",
    url="http://example.com/product/123",
    available=True,
)


@pytest.mark.anyio
@patch("app.services.kafka_producer.AIOKafkaProducer")
async def test_send_product_success(mock_aio_kafka_producer):  # <- FIX
    """Test successful message sending on the happy path."""
    mock_producer_instance = mock_aio_kafka_producer.return_value  # <- FIX
    mock_producer_instance.start = AsyncMock()
    mock_producer_instance.send_and_wait = AsyncMock()
    mock_producer_instance.stop = AsyncMock()
    service = KafkaProducerService()

    await service.start()
    await service.send_product(SAMPLE_LAPTOP)
    await service.stop()

    mock_producer_instance.start.assert_called_once()
    mock_producer_instance.send_and_wait.assert_called_once()
    mock_producer_instance.stop.assert_called_once()


@pytest.mark.anyio
@patch("app.services.kafka_producer.AIOKafkaProducer")
async def test_send_product_with_retries(mock_aio_kafka_producer):  # <- FIX
    """Test that the producer retries on failure and eventually succeeds."""
    mock_producer_instance = mock_aio_kafka_producer.return_value  # <- FIX
    mock_producer_instance.start = AsyncMock()
    mock_producer_instance.stop = AsyncMock()
    mock_producer_instance.send_and_wait.side_effect = [
        Exception("Kafka connection failed"),
        Exception("Kafka still down"),
        AsyncMock(),
    ]
    service = KafkaProducerService()

    await service.start()
    await service.send_product(SAMPLE_LAPTOP)
    await service.stop()

    assert mock_producer_instance.send_and_wait.call_count == 3
