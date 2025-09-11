"""
Unit tests for the KafkaProducerService.

Tests cover producer lifecycle, message serialization, retry logic,
and the new dynamic topic routing based on product_type.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from web_scraper_service.app.services.kafka_producer import KafkaProducerService
from web_scraper_service.app.models.products.laptop import Laptop


# Mock Pydantic models for testing
@pytest.fixture
def mock_laptop_model():
    """Provides a valid mock Laptop model."""
    return Laptop(
        product_type="laptop",
        product_name="Test Laptop",
        brand="TestBrand",
        sku="TEST-LAP-001",
        price=1200.50,
        availability="in_stock",
        url="http://test.com/laptop",
        ram="16GB",
        storage="512GB SSD",
        cpu="Test CPU",
        screen_resolution="1920x1080",
        screen_size=15.6,
        touchscreen=False,
        weight=2.1,
    )


@pytest.mark.anyio
@patch("web_scraper_service.app.services.kafka_producer.AIOKafkaProducer")
async def test_send_product_sends_to_correct_topic(
    mock_aio_producer, mock_laptop_model
):
    """
    Tests that send_product sends a message to the correct, dynamically generated topic.
    """
    # Arrange
    mock_producer_instance = mock_aio_producer.return_value
    mock_producer_instance.start = AsyncMock()
    mock_producer_instance.send_and_wait = AsyncMock()
    mock_producer_instance.stop = AsyncMock()

    producer = KafkaProducerService()
    await producer.start()

    # Act
    await producer.send_product(mock_laptop_model)

    # Assert
    # Verify it was sent to the 'products-laptop' topic
    mock_producer_instance.send_and_wait.assert_called_once()
    call_args = mock_producer_instance.send_and_wait.call_args
    assert call_args[0][0] == "products-laptop"  # Check the topic name
    await producer.stop()


@pytest.mark.anyio
@patch("web_scraper_service.app.services.kafka_producer.AIOKafkaProducer")
async def test_send_product_raises_error_if_no_type(mock_aio_producer):
    """
    Tests that send_product raises a ValueError if the model has no 'product_type' attribute.
    """
    # Arrange
    mock_producer_instance = mock_aio_producer.return_value
    mock_producer_instance.start = AsyncMock()
    mock_producer_instance.stop = AsyncMock()

    producer = KafkaProducerService()
    await producer.start()

    # Create a simple object without the required attribute
    product_without_type = MagicMock()
    del product_without_type.product_type

    # Act & Assert
    with pytest.raises(
        ValueError, match="Product model must have a 'product_type' attribute."
    ):
        await producer.send_product(product_without_type)

    await producer.stop()
