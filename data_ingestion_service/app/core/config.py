# File: app/core/config.py
"""Core application settings and configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines application settings, loaded from environment variables or a .env file.

    Attributes:
        DATABASE_URL: The connection string for the PostgreSQL database.
        KAFKA_BOOTSTRAP_SERVERS: The connection string for the Kafka cluster.
    """
    DATABASE_URL: str = "postgresql://admin:admin123@localhost:5432/e_database"

    # Add this line to match the variable in your .env file
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    # Configure Pydantic to load settings from a .env file.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()