"""Pydantic models for product data scraped from vendor websites.

Defines product schemas to ensure consistency, validation,
and structure before data is published to Kafka or used downstream.

Each product type (laptops, desktops, peripherals, etc.) uses this shared
model structure or an inherited subtype.

Belongs to: Data Modeling
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class BaseProduct(BaseModel):
    """Base Pydantic model for generic product data.

    All common fields and basic validation logic are defined here.
    Inherit from this class to define specific product categories.

    Attributes:
        name (str): Product name.
        sku (str): Stock Keeping Unit, must not be empty.
        price (float): Product price (must be positive).
        vendor (str): Vendor name.
        url (str): Product URL.
        available (bool): Availability status.
    """

    name: str = Field(..., description="Product name")
    sku: str = Field(..., description="Stock Keeping Unit, must not be empty")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    vendor: str = Field(..., description="Vendor name")
    url: str = Field(..., description="Product URL")
    available: bool = Field(True, description="Availability status")

    @validator("sku")
    def sku_must_not_be_empty(cls, v):
        """Ensures the SKU field is not empty.

        Args:
            v (str): SKU value.

        Returns:
            str: Validated SKU.

        Raises:
            ValueError: If SKU is empty.
        """
        if not v or not v.strip():
            raise ValueError("SKU must not be empty")
        return v


class LaptopProduct(BaseProduct):
    """Pydantic model for laptop products.

    Attributes:
        ram (Optional[str]): RAM specification.
        cpu (Optional[str]): CPU specification.
        screen_size (Optional[str]): Screen size.
        storage (Optional[str]): Storage capacity (e.g., 512GB SSD).
    """

    ram: Optional[str] = Field(None, description="RAM specification")
    cpu: Optional[str] = Field(None, description="CPU specification")
    screen_size: Optional[str] = Field(None, description="Screen size")
    storage: Optional[str] = Field(
        None, description="Storage capacity (e.g., 512GB SSD)"
    )


class DesktopProduct(BaseProduct):
    """Pydantic model for desktop products.

    Attributes:
        ram (Optional[str]): RAM specification.
        cpu (Optional[str]): CPU specification.
        form_factor (Optional[str]): Form factor (e.g., tower, mini).
        storage (Optional[str]): Storage capacity (e.g., 1TB HDD).
    """

    ram: Optional[str] = Field(None, description="RAM specification")
    cpu: Optional[str] = Field(None, description="CPU specification")
    form_factor: Optional[str] = Field(
        None, description="Form factor (e.g., tower, mini)"
    )
    storage: Optional[str] = Field(None, description="Storage capacity (e.g., 1TB HDD)")


class PeripheralProduct(BaseProduct):
    """Pydantic model for peripheral products (e.g., keyboard, mouse, monitor).

    Attributes:
        type (Optional[str]): Peripheral type (e.g., mouse, keyboard, monitor).
        interface (Optional[str]): Connection interface (e.g., USB, Bluetooth).
        compatibility (Optional[str]): Compatible devices or systems.
    """

    type: Optional[str] = Field(
        None, description="Peripheral type (e.g., mouse, keyboard, monitor)"
    )
    interface: Optional[str] = Field(
        None, description="Connection interface (e.g., USB, Bluetooth)"
    )
    compatibility: Optional[str] = Field(
        None, description="Compatible devices or systems"
    )
