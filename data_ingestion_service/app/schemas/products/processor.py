from .base_products import BaseProduct
from pydantic import Field
from typing import Optional


class Processor(BaseProduct):
    """
    Pydantic model for CPU (Processor) details.
    Inherits common product attributes from ProductBase.
    """

    socket_type: str = Field(..., min_length=1, description="CPU socket type.")
    core_count: int = Field(..., ge=1, description="Number of CPU cores.")
    thread_count: Optional[int] = Field(
        None, ge=1, description="Number of CPU threads."
    )
    base_clock_ghz: Optional[float] = Field(
        None, gt=0, description="Base clock speed in GHz."
    )
    boost_clock_ghz: Optional[float] = Field(
        None, gt=0, description="Max boots clock speed in GHz."
    )
    cache_mb: Optional[float] = Field(
        None, gt=0, description="Total cache size in MB (L2 + L3)."
    )
    integrated_graphics: Optional[str] = Field(
        None, min_length=1, description="Name of integrated graphics."
    )
