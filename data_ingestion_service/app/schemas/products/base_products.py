from pydantic import BaseModel, Field, field_validator, HttpUrl, ConfigDict
from typing import Optional, Literal
from enum import Enum
import re
from datetime import date


class Availability(str, Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    PREORDER = "preorder"
    DISCONTINUED = "discontinued"


class BaseProduct(BaseModel):
    """
    Base Pydantic model for a generic product.
    Includes common fields and basic validation rules.
    """

    # Use the modern ConfigDict for model configuration
    model_config = ConfigDict(extra="forbid")

    # --- THIS IS THE NEW FIELD ---
    product_type: Literal[
        "laptop",
        "desktop",
        "monitor",
        "tablet",
        "keyboard",
        "mouse",
        "processor",
        "ram",
        "storage",
        "gpu",
    ] = Field(..., description="The type of the product.")

    product_name: str = Field(
        ..., min_length=1, description="Full marketing name of the product."
    )
    model: Optional[str] = Field(
        None, min_length=1, description="Model number/name of the product."
    )
    brand: str = Field(..., min_length=1, description="Manufacturer or brand name.")
    sku: str = Field(..., description="Stock Keeping Unit.")
    price: float = Field(..., gt=0, description="Price of the product.")
    description: Optional[str] = Field(
        None, min_length=1, description="Description of the product."
    )
    availability: Optional[Availability]

    release_date: Optional[date] = Field(None, description="Product release date.")

    color: Optional[str] = Field(None, min_length=1)

    vendor: Optional[str] = Field(None, min_length=1, description="Product vendor.")

    url: HttpUrl = Field(..., description="URL link of the product.")

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, v: str):
        if not re.fullmatch(r"^[a-zA-Z0-9-]{5,50}$", v):
            raise ValueError(
                "SKU must contain only alphanumeric characters and hyphens, and be between 5 and 50 characters."
            )
        return v


class RAM(BaseModel):
    """
    Model representing RAM specifications.
    Includes capacity, type, speed, and module count.
    """

    capacity_gb: int = Field(..., gt=0, le=512, description="Total RAM size in GB.")
    type: Optional[str] = Field(None, min_length=1, description="e.g., DDR4, DDR5.")
    speed_mhz: Optional[int] = Field(None, gt=0, description="RAM speed in MHz.")
    module_count: Optional[int] = Field(
        None, ge=1, description="Number of RAM sticks/modules."
    )


class StorageModel(BaseModel):
    """
    Model representing storage device specifications.
    Includes capacity, storage type (HDD, SSD, etc.), and interface.
    """

    capacity_gb: int = Field(..., gt=0, le=16384, description="Storage capacity in GB.")
    type: Literal["HDD", "SSD", "NVMe", "eMMC", "Hybrid"] = Field(
        ..., description="Storage type."
    )
    interface: Optional[str] = Field(
        None, min_length=1, description="Connection interface."
    )


class GPU(BaseModel):
    """
    Model representing GPU specifications.
    Includes GPU model name, VRAM size, and manufacture
    """

    model: str = Field(..., min_length=1, description="GPU model name.")
    vram_gb: Optional[int] = Field(None, gt=0, description="Video RAM in GB.")
    manufacturer: Optional[str] = Field(
        None, min_length=1, description="e.g., NVIDIA, AMD, Intel."
    )
