"""
Pydantic models for the scraping API endpoints.

Defines the structure for API requests and responses, including
input validation for triggering scraping jobs.
"""

from pydantic import BaseModel, Field
import uuid


class ScrapeRequest(BaseModel):
    """Defines the request body for the POST /scrape endpoint."""

    vendor: str = Field(
        ...,
        json_schema_extra={"example": "vendor_a"},
        description="The registered name of the vendor to scrape (e.g., 'vendor_a').",
    )
    category: str = Field(
        ...,
        json_schema_extra={"example": "laptops"},
        description="The product category to scrape (e.g., 'laptops').",
    )


class ScrapeResponse(BaseModel):
    """Defines the response for a successfully accepted scraping job."""

    task_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        json_schema_extra={"example": "c2b2e8f8-52c5-4a6c-a2c1-8d3e3de17a23"},
        description="A unique ID for the accepted scraping task.",
    )
    status: str = Field("accepted", description="The status of the job request.")
    message: str = Field(
        ...,
        json_schema_extra={
            "example": "Scraping job for vendor 'vendor_a' and category 'laptops' has been accepted."
        },
        description="A descriptive message about the accepted job.",
    )
