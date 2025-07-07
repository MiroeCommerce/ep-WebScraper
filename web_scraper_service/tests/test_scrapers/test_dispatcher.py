# web_scraper_service/tests/test_scrapers/test_dispatcher.py

import pytest
from unittest.mock import AsyncMock, patch

from app.services.dispatcher import ScraperDispatcher


@pytest.mark.anyio
@patch("app.services.dispatcher.create_scraper")
@patch("app.services.dispatcher.KafkaProducerService")
async def test_dispatcher_pipeline_success(mock_kafka_producer, mock_create_scraper):
    """Test the full dispatcher pipeline on a successful run."""
    # Arrange
    producer_instance = mock_kafka_producer.return_value
    producer_instance.start = AsyncMock()
    producer_instance.send_product = AsyncMock()
    producer_instance.stop = AsyncMock()

    mock_scraper = mock_create_scraper.return_value
    mock_scraper.fetch_html.return_value = "<html>Success</html>"

    mock_scraper.parse_html.return_value = {
        "name": "Mock Product",
        "sku": "MOCK123",
        "price": 999.0,
        "vendor": "MockVendor",
        "url": "http://example.com/success",
        "available": True,
    }

    dispatcher = ScraperDispatcher()

    # Act
    await dispatcher.process_product_scraping("vendor_a", "http://example.com/success")

    # Assert: Now this will pass because validation succeeds
    producer_instance.start.assert_called_once()
    producer_instance.send_product.assert_called_once()
    producer_instance.stop.assert_called_once()
