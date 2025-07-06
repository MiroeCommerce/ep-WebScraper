import json
import anyio
import pytest
from unittest.mock import patch
from aiokafka import AIOKafkaConsumer
from app.services.dispatcher import ScraperDispatcher
from app.core.config import settings


@pytest.mark.integration
@pytest.mark.anyio
async def test_end_to_end_dispatcher_pipeline(
    anyio_backend,
):  # <-- Add the 'anyio_backend' fixture
    """
    Tests the full pipeline. Skips on the 'trio' backend due to an
    incompatibility with the aiokafka library.
    """
    # This is the crucial line:
    if anyio_backend == "trio":
        pytest.skip("aiokafka is incompatible with the trio backend in this test.")

    # ARRANGE
    mock_product_data = {
        "name": "Integration Test Laptop",
        "sku": "INT-TEST-LAPTOP-001",
        "price": 1234.56,
        "vendor": "IntegrationTestVendor",
        "url": "http://integration.test/laptop",
        "available": True,
    }

    async with AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        group_id="integration_test_group_final",
    ) as consumer:
        await consumer.seek_to_end()
        with patch("app.services.dispatcher.create_scraper") as mock_create_scraper:
            mock_scraper = mock_create_scraper.return_value
            mock_scraper.fetch_html.return_value = "<html></html>"
            mock_scraper.parse_html.return_value = mock_product_data
            dispatcher = ScraperDispatcher()
            await dispatcher.process_product_scraping(
                "mock_vendor", "http://integration.test/laptop"
            )
        try:
            with anyio.fail_after(5):
                message = await consumer.getone()
        except TimeoutError:
            message = None

        assert message is not None, "Did not receive a message from Kafka in time."

        received_data = json.loads(message.value.decode("utf-8"))

        assert received_data["sku"] == mock_product_data["sku"]
        assert received_data["price"] == pytest.approx(mock_product_data["price"])
