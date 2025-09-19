import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from data_ingestion_service.app.consumers.kafka_consumer import ProductConsumer



@pytest.mark.asyncio
async def test_process_message_success():
    consumer = ProductConsumer()

    message = {
        'product_name': 'Test Mouse',
        'product_type': 'mouse',
        'brand': 'Brand',
        'sku': 'testsku1',
        'price': 10.9,
        'url': "https://test.com/",
        'availability': None

    }

    topic = f"{consumer.topic_prefix}-mouse"

    mock_session = AsyncMock()
    mock_db = MagicMock()
    mock_db.session_scope.return_value.__aenter__.return_value = mock_session
    mock_db.session_scope.return_value.aexit__.return_value = None
    consumer.db = mock_db

    with patch("data_ingestion_service.app.crud.ProductCRUD.process_product", new_callable=AsyncMock) as mock_create:
        with patch("data_ingestion_service.app.crud.CategoryCRUD.get_or_create_category", new_callable=AsyncMock) as mock_category:
            await consumer.process_message(json.dumps(message).encode(), topic)

            mock_category.assert_called_once_with("mouse")
            mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_consume_loop_commits_batch():
    consumer = ProductConsumer()
    consumer._consumer = AsyncMock()

    message = MagicMock()
    message.value = json.dumps({
        'product_name': 'Test Mouse',
        'product_type': 'mouse',
        'brand': 'Brand',
        'sku': 'testsku1',
        'price': 10.9,
        'url': "https://test.com/",
        'availability': None

    }).encode()
    message.topic = 'products-mouse'

    message2 = MagicMock()
    message2.value = json.dumps({
        'product_name': 'Test Keyboard',
        'product_type': 'keyboard',
        'brand': 'Brand',
        'sku': 'testsku2',
        'price': 19.9,
        'url': "https://test.com/",
        'availability': None

    }).encode()
    message2.topic = 'products-keyboard'

    consumer._consumer.__aiter__.return_value = [message, message2]
    consumer._consumer.commit = AsyncMock()

    with patch.object(consumer, 'process_message', new_callable=AsyncMock):
        await consumer.consume(commit_interval=2)

    consumer._consumer.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_message_unknown_topic():
    consumer = ProductConsumer()
    topic = f"{consumer.topic_prefix}-unknown"

    message = json.dumps({'test': 'test'}).encode()

    mock_db = MagicMock()
    consumer.db = mock_db

    with patch('data_ingestion_service.app.consumers.kafka_consumer.logger', new_callable=AsyncMock) as mock_logger:
        await consumer.process_message(msg=message, topic=topic)

        mock_logger.warning.assert_called_with(f"No Pydantic model for topic {topic}.")
        mock_db.session_scope.return_value.__aenter__.return_value.add_assert_not_called()