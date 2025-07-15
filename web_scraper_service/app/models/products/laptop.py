from .base_products import BaseProduct, GPU, RAM, StorageModel
from .processor import Processor
from typing import Union, Optional, List
from pydantic import Field


class Laptop(BaseProduct):
    """
    Pydantic model for Laptop details.
    Inherits common product attributes from ProductBase.
    """

    ram: Union[List[RAM], str] = Field(..., description="RAM configuration.")
    storage: Union[List[StorageModel], str] = Field(
        ..., description="Storage configuration."
    )
    cpu: Union[Processor, str] = Field(..., description="CPU details or name.")
    os: Optional[str] = Field(None, min_length=1, description="Operating system.")
    graphics: Optional[Union[GPU, str]] = Field(
        None, description="Discrete or integrated GPU model."
    )

    screen_resolution: str = Field(..., min_length=1, description="Screen resolution.")
    screen_size: float = Field(..., gt=0, description="Screen size in inches.")
    touchscreen: bool = Field(
        ..., description="Indicates if the display is a touchscreen."
    )
    weight: float = Field(..., gt=0, description="Weight of laptop in kg/lbs.")
    battery_life: Optional[float] = Field(
        None, gt=0, description="Average battery life in hours."
    )
    keyboard_backlit: Optional[bool] = Field(
        False, description="Whether the keyboard is backlit."
    )
    webcam: Optional[bool] = Field(None, description="Built-in webcam presence.")
    webcam_resolution: Optional[str] = Field(
        None, min_length=1, description="Webcam resolution."
    )
    ports: List[str] = Field(
        default_factory=list, description="List of available ports."
    )
    form_factor: Optional[str] = Field(
        None, min_length=1, description="Laptop form factor."
    )
    fingerprint_reader: Optional[bool] = Field(
        None, description="Indicates if it has a fingerprint reader."
    )
