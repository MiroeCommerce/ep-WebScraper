from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB  # Use JSONB for efficiency in PostgreSQL
from ..core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    price = Column(Float, nullable=False)
    url = Column(String)  # Add the URL field

    # Column for storing nested specifications like RAM, GPU, etc.
    specifications = Column(JSONB)

    # Foreign Key for Vendor
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    vendor = relationship("Vendor")

    # Foreign Key for Category
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")