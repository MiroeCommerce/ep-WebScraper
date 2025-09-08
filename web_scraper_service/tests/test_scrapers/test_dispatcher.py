"""Unit tests for the ScraperDispatcher pipeline.

Covers the dispatcher workflow: scraper creation, product parsing,
and publishing data to Kafka with successful run simulation.
"""

import pytest
from unittest.mock import AsyncMock, patch
from web_scraper_service.app.services.dispatcher import ScraperDispatcher
from web_scraper_service.app.models.products.laptop import Laptop


@pytest.mark.anyio
@patch("web_scraper_service.app.services.dispatcher.create_scraper")
@patch("web_scraper_service.app.services.dispatcher.KafkaProducerService")
# Patch is no longer needed here as the dispatcher doesn't import this script.
# @patch(
#     "web_scraper_service.scripts.create_kafka_topics.create_topic",
#     new_callable=AsyncMock,
# )
async def test_dispatcher_pipeline_success(
    mock_kafka_producer_cls, mock_create_scraper_factory
):
    """Tests that the dispatcher pipeline runs successfully.

    Mocks the Kafka producer and scraper, then verifies that
    the pipeline starts, parses, validates, and sends product data as expected.

    Args:
        mock_kafka_producer_cls: The patched KafkaProducerService class.
        mock_create_scraper_factory: The patched create_scraper factory function.
    """
    # Arrange
    producer_instance = mock_kafka_producer_cls.return_value
    producer_instance.start = AsyncMock()
    producer_instance.send_product = AsyncMock()
    producer_instance.stop = AsyncMock()

    mock_scraper = mock_create_scraper_factory.return_value
    mock_scraper.fetch_html.return_value = "<html>Success</html>"

    # Updated mock data to match the new Laptop model and include product_type
    mock_scraper.parse_html.return_value = {
        "product_type": "laptop",
        "product_name": "Mock Laptop",
        "brand": "MockBrand",
        "sku": "MOCK-LAP-123",
        "price": 999.0,
        "availability": "in_stock",
        "url": "http://example.com/success",
        "ram": "16GB DDR5",
        "storage": "1TB NVMe SSD",
        "cpu": "Mock CPU i9",
        "screen_resolution": "1920x1080",
        "screen_size": 15.6,
        "touchscreen": False,
        "weight": 1.8,
    }

    dispatcher = ScraperDispatcher(kafka_producer=producer_instance)

    # Act
    # Call the method with the new 'category' argument
    await dispatcher.process_product_scraping(
        scraper_name="vendor_a", url="http://example.com/success", category="laptops"
    )

    # Assert
    producer_instance.start.assert_called_once()
    producer_instance.send_product.assert_called_once()
    producer_instance.stop.assert_called_once()

    # Verify that send_product was called with a valid Laptop instance
    sent_product = producer_instance.send_product.call_args[0][0]
    assert isinstance(sent_product, Laptop)
    assert sent_product.sku == "MOCK-LAP-123"
    assert sent_product.product_type == "laptop"
