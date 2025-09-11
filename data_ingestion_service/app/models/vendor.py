"""SQLAlchemy ORM model for the 'vendors' table."""

import datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, func
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class Vendor(Base):
    """
    Represents a product vendor in the 'vendors' table.

    Attributes:
        vendor_id: The primary key for the vendor.
        name: The name of the vendor (unique).
        registration_date: The date the vendor was registered.
        status: The current status of the vendor (e.g., 'active').
        category_id: An integer field for legacy categorization.
        created_at: Timestamp of when the record was created.
        updated_at: Timestamp of the last update to the record.
    """
    __tablename__ = 'vendors'

    vendor_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    registration_date = Column(Date, nullable=False, default=datetime.date.today)
    status = Column(String(50), default='active')
    category_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # The relationship to 'Product' is defined using a string.
    # This prevents a circular import error since Product will import Vendor.
    products = relationship("Product", back_populates="vendor")
