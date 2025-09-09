"""Database model for product categories.

This module defines the `Category` model, which represents a product category
in the database (e.g., 'Laptops', 'Monitors'). It uses SQLAlchemy to map the
class to the 'categories' database table and defines its relationship to
the Product model.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base


class Category(Base):
    """Represents a product category in the database.

    This SQLAlchemy model maps to the 'categories' table. Each category has a
    unique name to prevent duplicates and is linked to the products that
    belong to it.

    Attributes:
        id (int): The primary key for the category.
        name (str): The unique name of the category (e.g., "Laptops").
        products (relationship): A SQLAlchemy relationship that provides access
            to all Product objects associated with this category.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Establish a one-to-many relationship with the Product model.
    # The 'back_populates' argument ensures that this relationship is mirrored
    # on the Product model under the 'category' attribute.
    products = relationship("Product", back_populates="category")

