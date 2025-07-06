"""Configuration module for the Web Scraper Microservice.

Uses Pydantic's BaseSettings to load configuration from environment
variables or a .env file. Centralizes settings for Kafka, logging, scheduling,
and service-specific parameters.

Settings can be accessed globally via: `from app.core.config import settings`

Belongs to: Core Configuration
"""

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables or a .env file.

    Attributes:
        KAFKA_BOOTSTRAP_SERVERS (str): Kafka broker addresses.
        KAFKA_TOPIC (str): Kafka topic for product data messages.
        KAFKA_MAX_RETRIES (int): Maximum number of Kafka send retries.
    """

    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        "localhost:9092", description="Kafka broker addresses."
    )

    KAFKA_TOPIC: str = Field("products", description="Kafka topic for product data.")

    KAFKA_MAX_RETRIES: int = Field(
        3, description="Maximum number of Kafka send retries."
    )

    class Config:
        """Pydantic config for Settings.

        Attributes:
            env_file (str): Path to the .env file.
            env_file_encoding (str): Encoding for the .env file.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings object
settings = Settings()
