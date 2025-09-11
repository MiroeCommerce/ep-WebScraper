# File: app/models/product.py
"""SQLAlchemy ORM model for the 'products' table."""

import uuid
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Numeric, Uuid, func, Integer, JSON
)
from sqlalchemy.orm import relationship

# No longer need the postgresql-specific JSONB
# from sqlalchemy.dialects.postgresql import JSONB

from ..core.database import Base


class Product(Base):
    """
    Represents a product in the 'products' table.

    This is the central model that links to vendors and categories.

    Attributes:
        product_id: The primary key for the product.
        name: The name of the product.
        sku: The unique stock keeping unit for the product.
        description: A text description of the product.
        status: The current status of the product (e.g., 'active').
        price: The price of the product.
        specs: A flexible JSON field for product specifications.
        vendor_id: Foreign key linking to the 'vendors' table.
        category_id: Foreign key linking to the 'product_categories' table.
    """
    __tablename__ = 'products'

    product_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default='active')
    price = Column(Numeric(10, 2), nullable=False, default=0.00)

    # Use the generic JSON type which works with both PostgreSQL and SQLite
    specs = Column(JSON)

    # Foreign keys linking to the other tables
    vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'), nullable=False)
    category_id = Column(Uuid(as_uuid=True), ForeignKey('product_categories.category_id'), nullable=False)

    # Relationships that link to the Vendor and ProductCategory ORM classes
    vendor = relationship("Vendor", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

