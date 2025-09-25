# File: app/crud.py
"""
Data Access Layer for creating and updating database records.

This module contains the business logic for ingesting product data,
including handling related entities like vendors and categories.
"""

import json

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductCategory,
    ProductVariant,
)

from data_ingestion_service.app.core.logger import logger


class ProductCRUD:
    """
    CRUD operations for managing products, product variant and product attributes.

    Provides methods for retrieving, creating, and updating product data
    as well as handling associated variants and attributes.

    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product(self, product_sku) -> Product:
        """
        Retrieve a product by SKU.

        Args:
            product_sku (str): The product's unique SKU.

        Returns:
            Product | None: The product instance if found, otherwise None.
        """
        stmt = select(Product).where(Product.sku == product_sku)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()

        return product

    async def update_product(self, product_data, product) -> Product:
        """
        Update an existing product and its variants.

        Args:
            product_data: Pydantic model containing validated product data.
            product (Product): Existing product instance to update.

        Returns:
            Product: The updated product instance.
        """
        product.name = product_data.product_name
        product.description = product_data.description

        await self.get_or_create_variant(product_data=product_data, product=product)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_or_create_variant(self, product_data, product) -> ProductVariant:
        """
        Retrieve or create a product variant for a given product.

        Args:
            product_data: Pydantic model containing validated product data.
            product (Product): The parent product instance.

        Returns:
            ProductVariant: The existing or newly created product variant.
        """
        stmt = select(ProductVariant).where(ProductVariant.sku == product_data.sku)
        result = await self.session.execute(stmt)
        variant = result.scalar_one_or_none()

        if not variant:
            variant_name = product_data.model
            price = product_data.price

            variant = ProductVariant(
                product_id=product.product_id,
                variant_name=variant_name,
                sku=product_data.sku,
                price=price,
            )

            self.session.add(variant)
            await self.session.flush()

        standard_fields = {
            "sku",
            "name",
            "product_name",
            "product_type",
            "price",
            "description",
            "availability",
            "model",
        }

        for key, value in product_data.model_dump().items():
            if key in standard_fields or value is None:
                continue

            attribute = await self.get_or_create_attribute(key, value)

            await self.update_or_create_attribute_value(
                value=value, attribute=attribute, variant=variant
            )

        return variant

    async def get_or_create_attribute(self, key, value) -> ProductAttribute:
        """
        Retrieve or create a product attribute.

        Args:
            key (str): Attribute name.
            value (Any): Attribute value, used to infer data type.

        Returns:
            ProductAttribute: The existing or newly created attribute.
        """
        normalized_code = slugify(key).replace("-", "_")

        stmt = select(ProductAttribute).where(ProductAttribute.code == normalized_code)
        result = await self.session.execute(stmt)
        attribute = result.scalar_one_or_none()

        if attribute:
            return attribute

        new_attribute = ProductAttribute(
            name=key.strip().title(), code=normalized_code, data_type=type(value)
        )

        self.session.add(new_attribute)
        await self.session.flush()

        return new_attribute

    async def update_or_create_attribute_value(
        self, value, attribute, variant
    ) -> ProductAttributeValue:
        """
        Create or update a product attribute value for a specific variant.

        Args:
            value (Any): The attribute's value.
            attribute (ProductAttribute): The related attribute definition.
            variant (ProductVariant): The product variant.

        Returns:
            ProductAttributeValue: The created or updated attribute value.
        """
        stmt = (
            select(ProductAttributeValue)
            .where(ProductAttributeValue.variant_id == variant.variant_id)
            .where(ProductAttributeValue.attribute_id == attribute.attribute_id)
        )

        result = await self.session.execute(stmt)
        attribute_value = result.scalar_one_or_none()

        value_text = (
            json.dumps(value) if isinstance(value, (list, dict)) else str(value)
        )

        if not attribute_value:
            new_attr_value = ProductAttributeValue(
                variant_id=variant.variant_id,
                attribute_id=attribute.attribute_id,
                value_text=value_text,
            )

            self.session.add(new_attr_value)
            await self.session.flush()

            return new_attr_value

        else:
            if not value_text == attribute_value.value_text:
                attribute_value.value_text = value_text
                await self.session.flush()

            return attribute_value

    async def create_product(self, product_data) -> Product:
        """
        Create a new product with variants and attributes.

        Args:
            product_data: Pydantic model containing validated product data.

        Returns:
            Product: The newly created product instance.

        Raises:
            IntegrityError: If a uniqueness constraint is violated.
            SQLAlchemyError: For other database errors.
        """
        try:
            product_name = product_data.product_name
            product_sku = product_data.sku
            product_description = product_data.description

            new_product = Product(
                name=product_name, sku=product_sku, description=product_description
            )

            self.session.add(new_product)
            await self.session.flush()

            await self.get_or_create_variant(
                product_data=product_data, product=new_product
            )

            await self.session.commit()
            await self.session.refresh(new_product)
            return new_product

        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Integrity error : {e}")
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error : {e}")
            raise e

    async def process_product(self, product_data):
        """
         Create or update a product based on existence.

        Args:
            product_data: Pydantic model containing validated product data.

        Returns:
            str: "updated" if the product was updated,
                 "created" if a new product was created.
        """
        product = await self.get_product(product_data.sku)

        if product:
            await self.update_product(product_data=product_data, product=product)
            return "updated"
        else:
            await self.create_product(product_data=product_data)
            return "created"


class CategoryCRUD:
    def __init__(self, session: AsyncSession):
        """
        CRUD operations for managing product categories.
        """
        self.session = session

    async def get_or_create_category(
        self, category_name: str
    ) -> ProductCategory:  # May need to refactor for the parent_id
        """
        Retrieves a category by name or creates it if it does not exist.

        Args:
            category_name: The name of the category to find or create.

        Returns:
            The existing or newly created ProductCategory object.
        """

        stmt = select(ProductCategory).where(ProductCategory.name == category_name)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        if not category:
            slug = category_name.lower().replace(" ", "-")
            new_category = ProductCategory(name=category_name, slug=slug)
            self.session.add(new_category)
            try:
                await self.session.commit()
            except IntegrityError:
                await self.session.rollback()
                result = await self.session.execute(stmt)
                category = result.scalar_one()
            await self.session.refresh(new_category)
            return new_category
        return category
