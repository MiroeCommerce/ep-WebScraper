"""Unit tests for the ScraperDispatcher pipeline.

Covers the dispatcher workflow: scraper creation, product parsing,
and publishing data to Kafka with successful run simulation.
"""

import pytest
from unittest.mock import AsyncMock, patch
from web_scraper_service.app.services.dispatcher import ScraperDispatcher


@pytest.mark.anyio
@patch("web_scraper_service.app.services.dispatcher.create_scraper")
@patch("web_scraper_service.app.services.dispatcher.KafkaProducerService")
# Patch create_topic to prevent the "was never awaited" warning.
# This ensures that if KafkaProducerService or any other dependency
# implicitly calls create_topic, it's handled by an AsyncMock.
@patch(
    "web_scraper_service.scripts.create_kafka_topics.create_topic",
    new_callable=AsyncMock,
)
# IMPORTANT: The arguments in the test function signature are in REVERSE order of the @patch decorators.
async def test_dispatcher_pipeline_success(
    mock_create_topic, mock_kafka_producer_cls, mock_create_scraper_factory
):
    """Tests that the dispatcher pipeline runs successfully.

    Mocks the Kafka producer and scraper, then verifies that
    the pipeline starts, parses, and sends product data as expected.

    Args:
        mock_create_topic: The patched create_topic function (to prevent unawaited coroutine warning).
        mock_kafka_producer_cls: The patched KafkaProducerService class.
        mock_create_scraper_factory: The patched create_scraper factory function.
    """
    # Arrange
    # Use mock_kafka_producer_cls to get the instance
    producer_instance = mock_kafka_producer_cls.return_value
    producer_instance.start = AsyncMock()
    producer_instance.send_product = AsyncMock()
    producer_instance.stop = AsyncMock()

    # Use mock_create_scraper_factory to get the instance
    mock_scraper = mock_create_scraper_factory.return_value
    mock_scraper.fetch_html.return_value = "<html>Success</html>"
    mock_scraper.parse_html.return_value = {
        "name": "Mock Product",
        "sku": "MOCK123",
        "price": 999.0,
        "vendor": "MockVendor",
        "url": "http://example.com/success",
        "available": True,
        "ram": "8GB",
        "cpu": "i5",
        "screen_size": "14 inch",
        "storage": "256GB SSD",
    }

    dispatcher = ScraperDispatcher()

    # Act
    await dispatcher.process_product_scraping("vendor_a", "http://example.com/success")

    # Assert
    producer_instance.start.assert_called_once()
    producer_instance.send_product.assert_called_once()
    producer_instance.stop.assert_called_once()
