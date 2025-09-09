"""Database model for product vendors.

This module defines the `Vendor` model, which represents a product vendor or
brand in the database (e.g., 'Intel', 'MugLife'). It uses SQLAlchemy to map
the class to the 'vendors' database table and defines its relationship to the
Product model.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base


class Vendor(Base):
    """Represents a product vendor in the database.

    This SQLAlchemy model maps to the 'vendors' table. Each vendor has a
    unique name to prevent duplicates and is linked to the products
    associated with it.

    Attributes:
        id (int): The primary key for the vendor.
        name (str): The unique name of the vendor (e.g., "Intel").
        products (relationship): A SQLAlchemy relationship providing access to
            all Product objects associated with this vendor.
    """
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Establish a one-to-many relationship with the Product model.
    # The 'back_populates' argument ensures that this relationship is mirrored
    # on the Product model under the 'vendor' attribute.
    products = relationship("Product", back_populates="vendor")
