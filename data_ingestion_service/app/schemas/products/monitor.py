from .base_products import BaseProduct
from typing import Optional, List
from pydantic import Field, field_validator, model_validator


class Monitor(BaseProduct):
    """
    Pydantic model for Monitor details.
    Inherits common product attributes from ProductBase.
    """

    screen_size: float = Field(..., gt=0, description="Screen size in inches.")
    response_time_ms: Optional[float] = Field(
        None, gt=0, description="Response time in milliseconds."
    )
    refresh_rate: Optional[int] = Field(
        None, gt=0, description="Max refresh rate in Hz."
    )
    panel_type: Optional[str] = Field(
        None, min_length=1, description="Panel technology."
    )
    glare_screen: Optional[str] = Field(
        None, min_length=1, description="Type of glare screen."
    )
    aspect_ratio: str = Field(..., min_length=1, description="Aspect ratio.")
    ports: List[str] = Field(
        default_factory=list, description="List of video input ports."
    )
    built_in_speakers: Optional[bool] = Field(
        False, description="Indicates if the monitor has built-in speakers."
    )
    dimensions_with_stand: str = Field(
        ...,
        min_length=1,
        description="Monitor dimensions (H x W x D) with stand in inches.",
    )
    dimensions_without_stand: str = Field(
        ...,
        min_length=1,
        description="Monitor dimensions (H x W x D) without stand in inches.",
    )
    weight_with_stand: float = Field(
        ..., gt=0, description="Monitor weight in lbs/kg with stand."
    )
    weight_without_stand: float = Field(
        ..., gt=0, description="Monitor weight in lbs/kg without stand."
    )

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v):
        if v and not v.count(":") == 1:
            raise ValueError("Aspect ratio must be in format '16:9', '21:9', etc.")
        return v

    @model_validator(mode="after")
    def validate_weights(self):
        weight_without = self.weight_without_stand
        weight_with = self.weight_with_stand
        if weight_with < weight_without:
            raise ValueError("Weight with stand must be >= weight without stand.")
        return self
