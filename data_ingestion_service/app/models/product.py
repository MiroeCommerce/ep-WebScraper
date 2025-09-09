"""Database model for products.

This module defines the `Product` model using SQLAlchemy. It represents a
product in the database, storing core information like SKU, name, and price,
as well as detailed specifications in a JSONB field. It also defines the
many-to-one relationships with the `Vendor` and `Category` models.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..core.database import Base


class Product(Base):
    """Represents a product's data in the 'products' table.

    This SQLAlchemy model includes all essential fields for a product, with
    relationships established to vendors and categories. The `specifications`
    field uses PostgreSQL's JSONB type for efficient storage and querying of
    nested product attributes.

    Attributes:
        id (int): The primary key for the product.
        sku (str): The unique Stock Keeping Unit for the product. Indexed for
            fast lookups.
        name (str): The display name of the product. Indexed for searching.
        price (float): The retail price of the product.
        url (str): The URL to the product's page on the vendor's website.
        specifications (dict): A JSONB field to store nested key-value pairs of
            product specifications (e.g., RAM, CPU, screen size).
        vendor_id (int): Foreign key linking to the 'vendors' table.
        vendor (relationship): SQLAlchemy relationship to the parent `Vendor`
            object.
        category_id (int): Foreign key linking to the 'categories' table.
        category (relationship): SQLAlchemy relationship to the parent
            `Category` object.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    price = Column(Float, nullable=False)
    url = Column(String)

    # Use JSONB for efficient storage and querying of nested specifications.
    specifications = Column(JSONB)

    # Define the many-to-one relationship to the Vendor model.
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    vendor = relationship("Vendor", back_populates="products")

    # Define the many-to-one relationship to the Category model.
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
