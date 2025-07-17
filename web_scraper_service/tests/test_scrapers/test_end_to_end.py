"""Integration test for the end-to-end dispatcher and Kafka pipeline.

This test verifies the full pipeline from scraping product data to publishing
and consuming it through Kafka using a unique topic for isolation.
"""

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
    """Tests the complete dispatcher-to-Kafka pipeline integration.

    This test does the following:
      - Creates a unique Kafka topic for isolation.
      - Injects a mock scraper and a producer configured for the test topic.
      - Sends product data through the dispatcher.
      - Consumes the message from the unique Kafka topic and verifies the content.

    Skips the test on the 'trio' backend (aiokafka is not compatible with it).

    Args:
        anyio_backend (str): The async backend being used by pytest-anyio.

    Raises:
        AssertionError: If no message is received from Kafka in time, or if the
                        message content is invalid.
    """
    if anyio_backend == "trio":
        pytest.skip("aiokafka is not compatible with the trio backend")

    # ARRANGE
    # 1. Create a unique topic name to ensure test isolation.
    test_topic = f"test-topic-{uuid.uuid4()}"

    # 2. Define the mock data that our scraper will "produce".
    mock_product_data = {
        "name": "Integration Test Laptop",
        "sku": "INT-TEST-LAPTOP-001",
        "price": 1234.56,
        "vendor": "IntegrationTestVendor",
        "url": "http://integration.test/laptop",
        "available": True,
        "ram": "16GB",
        "cpu": "i9",
        "screen_size": "16 inch",
        "storage": "1TB SSD",
    }

    # 3. Inject a KafkaProducerService instance configured with our unique test topic.
    producer = KafkaProducerService(topic=test_topic)
    dispatcher = ScraperDispatcher(kafka_producer=producer)

    # 4. Create a consumer that listens only to our unique test topic.
    consumer = AIOKafkaConsumer(
        test_topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        group_id=f"integration-test-group-{uuid.uuid4()}",
    )
    await consumer.start()
    await consumer.seek_to_end()  # Ensure we only read new messages for this test run.

    # 5. Patch the scraper creation to control the data being "scraped".
    with patch(
        "web_scraper_service.app.services.dispatcher.create_scraper"
    ) as mock_create_scraper:
        mock_scraper_instance = MagicMock()
        mock_scraper_instance.fetch_html.return_value = "<html></html>"
        mock_scraper_instance.parse_html.return_value = mock_product_data
        mock_create_scraper.return_value = mock_scraper_instance

        # ACT: Run the dispatcher, which will use our injected producer and mocked scraper.
        await dispatcher.process_product_scraping(
            "mock_vendor", "http://integration.test/laptop"
        )

    # ASSERT: Verify that the correct message was received on the unique topic.
    try:
        with anyio.fail_after(10):  # Wait up to 10 seconds for the message.
            message = await consumer.getone()
    except TimeoutError:
        message = None
    finally:
        # Clean up the consumer to prevent resource leaks.
        await consumer.stop()

    assert message is not None, "Did not receive a message from Kafka in time."
    received_data = json.loads(message.value.decode("utf-8"))
    assert received_data["sku"] == mock_product_data["sku"]
    assert received_data["price"] == pytest.approx(mock_product_data["price"])
