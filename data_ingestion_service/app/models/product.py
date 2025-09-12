import uuid

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
    Text,
    func,
    ForeignKey,
    Numeric,
    Integer,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from data_ingestion_service.app.core.database import Base


class Product(Base):
    """
    Represents a product in the catalog.

    Attributes:
        product_id (UUID): Primary key, unique identifier for the product.
        name (str): Name of the product.
        sku (str): Unique stock-keeping unit identifier.
        description (str): Optional description of the product.
        status (str): Status of the product (e.g., 'active', 'inactive').
        created_at (datetime): Timestamp of when the product was created.
        updated_at (datetime): Timestamp of the last update.

    Relationships:
        variants (list[ProductVariant]): List of all variants associated with this product.
    """

    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    variants = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    """
    Represents a specific variant of a product.

    Attributes:
        variant_id (UUID): Primary key, unique identifier for the variant.
        product_id (UUID): Foreign key referencing the parent product.
        sku (str): SKU for this variant (may differ from parent product SKU).
        variant_name (str): Name/description for the variant.
        price (Decimal): Price of the variant.
        stock_quantity (int): Current stock level.
        is_active (bool): Whether the variant is active.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.

    Relationships:
        product (Product): The parent product of this variant.
        attribute_values (list[ProductAttributeValue]): List of attribute values associated with this variant.
    """

    __tablename__ = "product_variants"

    variant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False,
    )
    sku = Column(String(100), nullable=False)
    variant_name = Column(String(225))
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    product = relationship(
        "Product", back_populates="variants"
    )
    attribute_values = relationship(
        "ProductAttributeValue", back_populates="variant", cascade="all, delete-orphan"
    )


class ProductAttribute(Base):
    """
    Represents a product attribute that can be assigned to product variants.

    Attributes:
        attribute_id (UUID): Primary key, unique identifier for the attribute.
        name (str): Human-readable name of the attribute.
        code (str): Unique code for the attribute.
        data_type (str): Type of the attribute value ('string', 'number', 'boolean', etc.).
        is_variant_level (bool): Whether this attribute applies at the variant level.
        is_filterable (bool): Whether this attribute can be used in filters.
        is_required (bool): Whether this attribute is required.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.

    Relationships:
        attribute_values (list[ProductAttributeValue]): List of values assigned to this attribute across variants.
    """

    __tablename__ = "product_attributes"

    attribute_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    data_type = Column(String(50), nullable=False)
    is_variant_level = Column(Boolean, default=False)
    is_filterable = Column(Boolean, default=True)
    is_required = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    attribute_values = relationship(
        "ProductAttributeValue",
        back_populates="attribute",
        cascade="all, delete-orphan",
    )


class ProductAttributeValue(Base):
    """
    Represents the value of a specific attribute for a specific product variant.

    Attributes:
        value_id (UUID): Primary key, unique identifier for the attribute value.
        variant_id (UUID): Foreign key referencing the product variant.
        attribute_id (UUID): Foreign key referencing the product attribute.
        value_text (str): The actual value of the attribute (as text).
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.

    Relationships:
        variant (ProductVariant): The product variant this value belongs to.
        attribute (ProductAttribute): The attribute this value corresponds to.
    """

    __tablename__ = "product_attribute_values"
    __table_args__ = (
        UniqueConstraint("variant_id", "attribute_id", name="unique_variant_attribute"),
    )

    value_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("product_variants.variant_id", ondelete="CASCADE"),
        nullable=False,
    )
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("product_attributes.attribute_id", ondelete="CASCADE"),
        nullable=False,
    )
    value_text = Column(Text())
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    variant = relationship("ProductVariant", back_populates="attribute_values")
    attribute = relationship("ProductAttribute", back_populates="attribute_values")
