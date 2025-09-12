from .base_products import BaseProduct
from typing import Optional
from pydantic import Field


class Keyboard(BaseProduct):
    """
    Pydantic model for Keyboard details.
    Inherits common product attributes from BaseProduct.
    """

    layout: Optional[str] = Field(None, min_length=1, description="Keyboard layout.")
    mechanical: Optional[bool] = Field(
        False, description="Indicates if the keyboard is mechanical."
    )
    backlit: Optional[bool] = Field(
        False, description="Indicates if the keyboard has backlit keys."
    )
    wireless: Optional[bool] = Field(
        False, description="Indicates if the keyboard is wireless."
    )
    connection_type: Optional[str] = Field(
        None, description="Connection interface (e.g., USB, Bluetooth)."
    )
    key_count: Optional[int] = Field(
        None, gt=0, description="Number of keys on the keyboard."
    )
    dimensions: Optional[str] = Field(
        None,
        min_length=1,
        description="Physical dimensions (L x W x H) in cm or inches.",
    )
    weight: Optional[float] = Field(
        None, gt=0, description="Weight of the keyboard in kg/lbs."
    )
