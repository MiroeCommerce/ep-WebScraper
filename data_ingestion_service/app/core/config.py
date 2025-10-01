# File: app/core/config.py
"""Core application settings and configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """
    Defines application settings, loaded from environment variables or a .env file.

    Attributes:
        DATABASE_URL: The connection string for the PostgreSQL database.
        KAFKA_BOOTSTRAP_SERVERS: The connection string for the Kafka cluster.
    """

    DATABASE_URL: str = "postgresql+asyncpg://admin:admin123@localhost:5432/e_database"

    # Add this line to match the variable in your .env file

    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        "localhost:9092", description="Kafka broker addresses."
    )
    KAFKA_TOPIC_PREFIX: str = Field(
        "products", description="Default Kafka topic for product data."
    )
    KAFKA_CONSUMER_GROUP: str = Field(
        "data_ingestion_consumer_group", description="Kafka consumer group ID."
    )

    # Configure Pydantic to load settings from a .env file.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
