"""Kafka topic creation script for the Web Scraper Service.

This standalone script uses aiokafka's AdminClient to connect to a Kafka
broker and create a specified topic if it does not already exist. It is
designed to be run manually or as part of a setup process to ensure the
necessary Kafka infrastructure is in place.

This script is idempotent; it can be run multiple times without causing errors,
as it checks for the topic's existence before attempting creation.

Attributes:
    TOPIC_NAME (str): The default name of the Kafka topic to create.
    KAFKA_BOOTSTRAP_SERVERS (str): The address of the Kafka broker(s).
"""

import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

# --- Configuration ---
TOPIC_NAME: str = "products"
KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"


async def create_topic() -> None:
    """Creates the primary Kafka topic if it does not already exist.

    Connects to the Kafka cluster using an admin client, lists all topics,
    and if the target topic is not found, it creates it with default
    partition and replication factor settings.

    Side Effects:
        Prints the status of the topic creation (created or already exists)
        to standard output.

    Raises:
        KafkaConnectionError: If the admin client cannot connect to the
            bootstrap servers.
    """
    admin_client = None  # Initialize to ensure it's available in `finally`
    try:
        admin_client = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await admin_client.start()

        topics = await admin_client.list_topics()
        if TOPIC_NAME not in topics:
            await admin_client.create_topics(
                [NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)]
            )
            print(f"Topic '{TOPIC_NAME}' created.")
        else:
            print(f"Topic '{TOPIC_NAME}' already exists.")
    finally:
        # Ensure the admin client connection is always closed gracefully.
        if admin_client:
            await admin_client.close()


def main() -> None:
    """Main entry point for running the script."""
    print("Attempting to create Kafka topic...")
    asyncio.run(create_topic())


if __name__ == "__main__":
    main()
