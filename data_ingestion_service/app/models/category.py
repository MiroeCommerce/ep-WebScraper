"""SQLAlchemy ORM model for the 'product_categories' table."""

import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, Uuid, func
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class ProductCategory(Base):
    """
    Represents a product category in the 'product_categories' table.

    This table supports a hierarchical structure via the `parent_id` field.

    Attributes:
        category_id: The primary key for the category.
        name: The name of the category (e.g., "Laptops").
        parent_id: A foreign key for creating a category hierarchy.
        slug: A URL-friendly version of the category name.
        description: A text description of the category.
        is_active: Whether the category is currently active.
        created_at: Timestamp of when the record was created.
        updated_at: Timestamp of the last update to the record.
    """
    __tablename__ = 'product_categories'

    category_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True, index=True)
    parent_id = Column(Uuid(as_uuid=True), ForeignKey('product_categories.category_id'))
    slug = Column(String(255), unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Self-referencing relationship for parent/child categories.
    parent = relationship("ProductCategory", remote_side=[category_id])

    # Commenting out for now, no direct connection between the tables
    # Relationship to 'Product' is defined using a string to prevent circular imports.
    # products = relationship("Product", back_populates="category")
