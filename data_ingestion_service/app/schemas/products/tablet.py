from .base_products import BaseProduct, GPU, StorageModel, RAM
from .processor import Processor
from typing import Optional, List, Union
from pydantic import Field


class Tablet(BaseProduct):
    """
    Pydantic model for Tablet details.
    Inherits common product attributes from BaseProduct.
    """

    ram: Union[List[RAM], str] = Field(..., description="RAM configuration.")
    storage: Union[List[StorageModel], str] = Field(
        ..., description="Storage configuration."
    )
    cpu: Union[Processor, str] = Field(..., description="CPU details or name.")
    os: Optional[str] = Field(None, min_length=1, description="Operating system.")
    screen_size: float = Field(..., gt=0, description="Screen size in inches.")
    screen_resolution: Optional[str] = Field(
        None, min_length=1, description="Screen resolution."
    )
    battery_life: Optional[float] = Field(
        None, gt=0, description="Average battery life in hours."
    )
    weight: Optional[float] = Field(
        None, gt=0, description="Weight of tablet in kg/lbs."
    )
    stylus_support: Optional[bool] = Field(
        False, description="Indicates if tablet supports stylus input."
    )
    cellular: Optional[bool] = Field(
        False,
        description="Indicates if tablet supports cellular connectivity.",
    )
    ports: List[str] = Field(
        default_factory=list, description="List of available ports."
    )
