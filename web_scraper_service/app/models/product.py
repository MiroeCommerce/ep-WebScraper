"""
Pydantic models for product data scraped from vendor websites.

Defines the `Product` schema that ensures consistency, validation,
and structure before scraped data is published to Kafka or
passed to downstream systems.

Each product type like laptops, RAM, monitors uses this shared
model structure or a subtype if necessary.

Belongs to: Data Modeling
"""
