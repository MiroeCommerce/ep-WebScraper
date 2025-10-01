from .base_products import BaseProduct, GPU, RAM, StorageModel
from .processor import Processor
from typing import Union, Optional, List
from pydantic import Field


class Desktop(BaseProduct):
    """
    Pydantic model for Desktop details.
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
    form_factor: Optional[str] = Field(
        None, description="Desktop chassis form factor (e.g., Mini Tower, SFF, Micro)."
    )
    power_supply_watts: Optional[int] = Field(
        None, gt=0, description="Power supply rating in watts."
    )
    cooling_type: Optional[str] = Field(
        None, description="Cooling type (e.g., Air, Liquid)."
    )
    preinstalled_software: Optional[List[str]] = Field(
        default_factory=list, description="List of preinstalled software or bloatware."
    )
