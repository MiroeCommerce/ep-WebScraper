import json
import anyio
import pytest
import uuid
from unittest.mock import patch, MagicMock
from aiokafka import AIOKafkaConsumer
from web_scraper_service.app.services.dispatcher import ScraperDispatcher
from web_scraper_service.app.services.kafka_producer import KafkaProducerService
from web_scraper_service.app.core.config import settings


@pytest.mark.integration
@pytest.mark.anyio
async def test_end_to_end_dispatcher_pipeline(anyio_backend):
    if anyio_backend == "trio":
        pytest.skip("aiokafka is not compatible with the trio backend")

    # ARRANGE
    mock_product_data = {
        "product_type": "laptop",
        "product_name": "Integration Test Laptop",
        "brand": "IntegrationTestBrand",
        "sku": "INT-TEST-LAPTOP-001",
        "price": 1234.56,
        "availability": "in_stock",
        "url": "http://integration.test/laptop",
        "ram": "16GB",
        "storage": "1TB SSD",
        "cpu": "i9",
        "screen_resolution": "2560x1440",
        "screen_size": 16.0,
        "touchscreen": False,
        "weight": 1.9,
    }

    # FIX: KafkaProducerService no longer takes a 'topic' argument.
    producer = KafkaProducerService()
    dispatcher = ScraperDispatcher(kafka_producer=producer)

    test_topic = f"products-{mock_product_data['product_type']}"
    consumer = AIOKafkaConsumer(
        test_topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id=f"integration-test-group-{uuid.uuid4()}",
    )
    await consumer.start()

    with patch(
        "web_scraper_service.app.services.dispatcher.create_scraper"
    ) as mock_create_scraper:
        mock_scraper_instance = MagicMock()
        mock_scraper_instance.fetch_html.return_value = "<html></html>"
        mock_scraper_instance.parse_html.return_value = mock_product_data
        mock_create_scraper.return_value = mock_scraper_instance

        # ACT
        await dispatcher.process_product_scraping(
            "mock_vendor", "http://integration.test/laptop", "laptops"
        )

    # ASSERT
    try:
        with anyio.fail_after(10):
            message = await consumer.getone()
    except TimeoutError:
        message = None
    finally:
        await consumer.stop()

    assert message is not None, "Did not receive a message from Kafka in time."
    received_data = json.loads(message.value.decode("utf-8"))
    assert received_data["sku"] == mock_product_data["sku"]
    assert received_data["price"] == pytest.approx(mock_product_data["price"])
