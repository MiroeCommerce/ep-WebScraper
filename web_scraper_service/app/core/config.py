"""Configuration module for the Web Scraper Microservice."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv  # <-- Import the load_dotenv function

ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    print(f"--- Successfully loaded .env file from: {ENV_FILE_PATH} ---")
else:
    print(f"--- .env file not found at: {ENV_FILE_PATH}, using defaults. ---")


class Settings(BaseSettings):
    """Application settings loaded from environment variables or a .env file."""

    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        "localhost:9092", description="Kafka broker addresses."
    )
    KAFKA_TOPIC: str = Field("products", description="Kafka topic for product data.")
    KAFKA_MAX_RETRIES: int = Field(
        3, description="Maximum number of Kafka send retries."
    )

    SCHEDULER_CRON_HOUR: str = Field(
        "*", description="Cron expression for the hour to run the scraper."
    )
    SCHEDULER_CRON_MINUTE: str = Field(
        "0", description="Cron expression for the minute to run the scraper."
    )
    SCHEDULER_CRON_DAY_OF_WEEK: str = Field(
        "*", description="Cron expression for the day of the week to run the scraper."
    )
    SCHEDULER_JITTER: int = Field(
        300, description="Max seconds to randomly delay job execution."
    )

    # Pydantic will now read from the loaded environment variables.
    # The 'env_file' here is now more of a fallback.
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
