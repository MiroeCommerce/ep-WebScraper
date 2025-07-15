import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

TOPIC_NAME: str = "products"
KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"


async def create_topic() -> None:
    admin_client = None  # Initialize admin_client to None
    try:
        admin_client = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await admin_client.start()  # <-- MOVE THIS LINE INSIDE THE TRY BLOCK

        topics = await admin_client.list_topics()
        if TOPIC_NAME not in topics:
            await admin_client.create_topics(
                [NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)]
            )
            print(f"Topic '{TOPIC_NAME}' created.")
        else:
            print(f"Topic '{TOPIC_NAME}' already exists.")
    finally:
        if admin_client:  # <-- ADD THIS CHECK
            await admin_client.close()


def main() -> None:
    """Entrypoint for CLI execution."""
    asyncio.run(create_topic())


if __name__ == "__main__":
    main()
