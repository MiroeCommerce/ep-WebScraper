"""
Configuration module for the Web Scraper Microservice.

Uses Pydantic's BaseSettings to load configuration from environment
variables or a .env file. Centralizes settings for Kafka, logging, scheduling,
and service-specific parameters.

Settings can be accessed globally via: `from app.core.config import settings`

Belongs to: Core Configuration
"""
