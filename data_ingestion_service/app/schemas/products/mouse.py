from .base_products import BaseProduct
from typing import Optional
from pydantic import Field


class Mouse(BaseProduct):
    """
    Pydantic model for Mouse details.
    Inherits common product attributes from BaseProduct.
    """

    wireless: Optional[bool] = Field(
        False, description="Indicates if the mouse is wireless."
    )
    dpi: Optional[int] = Field(None, gt=0, description="Mouse sensitivity in DPI.")
    buttons_count: Optional[int] = Field(
        None, gt=0, description="Number of buttons on the mouse."
    )
    connection_type: Optional[str] = Field(None, description="Connection interface.")
    ergonomic: Optional[bool] = Field(
        False, description="Indicates if the mouse is ergonomically designed."
    )
    weight: Optional[float] = Field(None, gt=0, description="Weight of the mouse.")
    dimensions: Optional[str] = Field(
        None,
        min_length=1,
        description="Physical dimensions (L x W x H) in  inches.",
    )
