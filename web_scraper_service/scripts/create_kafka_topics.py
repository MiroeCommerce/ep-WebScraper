"""Kafka topic creation script for the Web Scraper Service.

Uses aiokafka's AdminClient to create the required Kafka topic
if it does not already exist. Can be run as a standalone script.

Belongs to: Infrastructure / DevOps Utilities
"""

import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

TOPIC_NAME: str = "products"
KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"


async def create_topic() -> None:
    """Creates a Kafka topic if it does not already exist.

    Uses aiokafka.admin.AIOKafkaAdminClient to list existing topics and
    creates the topic if missing.

    Raises:
        Exception: On Kafka connection or admin errors.
    """
    admin_client = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await admin_client.start()
    try:
        topics = await admin_client.list_topics()
        if TOPIC_NAME not in topics:
            await admin_client.create_topics(
                [NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)]
            )
            print(f"Topic '{TOPIC_NAME}' created.")
        else:
            print(f"Topic '{TOPIC_NAME}' already exists.")
    finally:
        await admin_client.close()


def main() -> None:
    """Entrypoint for CLI execution."""
    asyncio.run(create_topic())


if __name__ == "__main__":
    main()
