"""Unit tests for the CRUD operations in the Data Ingestion Service."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from slugify import slugify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from data_ingestion_service.app.crud import ProductCRUD, CategoryCRUD
from data_ingestion_service.app.models.product import (
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductVariant,
)
from data_ingestion_service.app.models.category import ProductCategory
from data_ingestion_service.app.schemas.products.base_products import Availability
from data_ingestion_service.app.schemas.products.mouse import Mouse


@pytest_asyncio.fixture
async def mock_session():
    session = AsyncMock()
    return session


@pytest_asyncio.fixture
async def mock_crud(mock_session):
    return ProductCRUD(session=mock_session)


@pytest.mark.asyncio
async def test_get_product_return_product(mock_session, mock_crud):
    existing_product = Product(product_id=1, name="Laptop", sku="testsku1")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_product
    mock_session.execute = AsyncMock(return_value=mock_result)

    product = await mock_crud.get_product("testsku1")

    assert product is existing_product
    assert product.name == existing_product.name
    assert product.product_id == existing_product.product_id


@pytest.mark.asyncio
async def test_get_product_return_None(mock_session, mock_crud):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    product = await mock_crud.get_product("tetsku2")

    assert product is None


@pytest.mark.asyncio
async def test_get_existing_attribute(mock_session, mock_crud):
    key = "color"
    value = "black"

    existing_attribute = ProductAttribute(
        attribute_id=1, name=key, code=key, data_type=str
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_attribute
    mock_session.execute = AsyncMock(return_value=mock_result)

    attribute = await mock_crud.get_or_create_attribute(key=key, value=value)

    assert attribute is existing_attribute
    assert attribute.attribute_id == existing_attribute.attribute_id
    mock_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_create_new_attribute(mock_session, mock_crud):
    key = "weight"
    value = "0.5kg"
    code = slugify(key).replace("-", "_")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    attribute = await mock_crud.get_or_create_attribute(key=key, value=value)

    assert isinstance(attribute, ProductAttribute)
    assert attribute.name == key.strip().title()
    assert attribute.code == code
    mock_session.add.assert_called_once_with(attribute)


@pytest.mark.asyncio
async def test_create_new_attribute_value(mock_session, mock_crud):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    attribute = ProductAttribute(
        attribute_id=1, name="weight", code="weight", data_type="str"
    )
    variant = ProductVariant(
        variant_id=1,
        product_id=1,
        sku="testsku",
        variant_name="Test Variant",
        price="11.11",
    )
    value = "0.5kg"

    new_attribute_value = await mock_crud.update_or_create_attribute_value(
        value=value, attribute=attribute, variant=variant
    )

    assert isinstance(new_attribute_value, ProductAttributeValue)
    assert new_attribute_value.attribute_id == 1
    assert new_attribute_value.variant_id == 1
    mock_session.add.assert_called_once_with(new_attribute_value)


@pytest.mark.asyncio
async def test_update_attribute_value(mock_session, mock_crud):
    existing_attr_value = ProductAttributeValue(
        value_id=1, variant_id=1, attribute_id=1, value_text="black"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_attr_value
    mock_session.execute = AsyncMock(return_value=mock_result)

    variant = AsyncMock()
    attribute = AsyncMock()
    new_value = "red"

    updated_attr_value = await mock_crud.update_or_create_attribute_value(
        value=new_value, attribute=attribute, variant=variant
    )

    assert isinstance(updated_attr_value, ProductAttributeValue)
    assert updated_attr_value.value_text == new_value
    mock_session.flush_assert_called_once()


@pytest.mark.asyncio
async def test_create_new_variant(mock_session, mock_crud):
    product_data = Mouse(
        product_type="mouse",
        product_name="Mouse Test",
        model="Test Mouse",
        brand="Brand",
        sku="testsku1",
        price=9.99,
        availability=Availability.IN_STOCK,
        url="https://test.com/",
    )
    product = Product(product_id=1, name="Mouse", sku="test_sku2")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    mock_crud.get_or_create_attribute = AsyncMock(
        return_value=ProductAttribute(attribute_id=1, name="brand", code="brand")
    )
    mock_crud.update_or_create_attribute_value = AsyncMock(
        return_value=ProductAttributeValue(
            value_id=1, variant_id=1, attribute_id=1, value_text="Brand"
        )
    )

    new_variant = await mock_crud.get_or_create_variant(
        product_data=product_data, product=product
    )

    assert isinstance(new_variant, ProductVariant)
    assert new_variant.sku == "testsku1"
    assert new_variant.variant_name == "Test Mouse"
    mock_session.add.assert_called_once_with(new_variant)


@pytest.mark.asyncio
async def test_create_new_product(mock_session, mock_crud):
    product_data = Mouse(
        product_type="mouse",
        product_name="Mouse Test",
        model="Test Mouse",
        brand="Brand",
        sku="testsku1",
        price=9.99,
        availability=Availability.IN_STOCK,
        url="https://test.com/",
        description="Test Mouse by Brand",
    )

    mock_crud.get_or_create_attribute = AsyncMock(
        return_value=ProductAttribute(attribute_id=1, name="brand", code="brand")
    )
    mock_crud.update_or_create_attribute_value = AsyncMock(
        return_value=ProductAttributeValue(
            value_id=1, variant_id=1, attribute_id=1, value_text="Brand"
        )
    )

    mock_crud.create_new_variant = AsyncMock(
        return_value=ProductVariant(
            variant_id=1, product_id=1, sku="testsku1", variant_name="Test Mouse"
        )
    )

    new_product = await mock_crud.create_product(product_data)

    assert isinstance(new_product, Product)
    assert new_product.name == "Mouse Test"
    mock_session.add.assert_called_once_with(new_product)


@pytest.mark.asyncio
async def test_create_product_integrity_error(mock_session, mock_crud):
    mock_session.flush = AsyncMock(
        side_effect=IntegrityError(
            statement="Database Integrity error", params={}, orig=None
        )
    )

    product_data = Mouse(
        product_type="mouse",
        product_name="Mouse Test",
        model="Test Mouse",
        brand="Brand",
        sku="testsku1",
        price=9.99,
        availability=Availability.IN_STOCK,
        url="https://test.com/",
        description="Test Mouse by Brand",
    )

    mock_crud.get_or_create_attribute = AsyncMock(
        return_value=ProductAttribute(attribute_id=1, name="brand", code="brand")
    )
    mock_crud.create_attribute_value = AsyncMock(
        return_value=ProductAttributeValue(
            value_id=1, variant_id=1, attribute_id=1, value_text="Brand"
        )
    )

    mock_crud.create_new_variant = AsyncMock(
        return_value=ProductVariant(
            variant_id=1, product_id=1, sku="testsku1", variant_name="Test Mouse"
        )
    )

    with pytest.raises(IntegrityError) as err_info:
        await mock_crud.create_product(product_data)

    mock_session.add.assert_called_once()
    assert "Database Integrity error" in str(err_info.value)


@pytest.mark.asyncio
async def test_create_product_sqlalchemy_error(mock_session, mock_crud):
    mock_session.flush = AsyncMock(side_effect=SQLAlchemyError("Error"))

    product_data = Mouse(
        product_type="mouse",
        product_name="Mouse Test",
        model="Test Mouse",
        brand="Brand",
        sku="testsku1",
        price=9.99,
        availability=Availability.IN_STOCK,
        url="https://test.com/",
        description="Test Mouse by Brand",
    )

    mock_crud.get_or_create_attribute = AsyncMock(
        return_value=ProductAttribute(attribute_id=1, name="brand", code="brand")
    )
    mock_crud.update_or_create_attribute_value = AsyncMock(
        return_value=ProductAttributeValue(
            value_id=1, variant_id=1, attribute_id=1, value_text="Brand"
        )
    )

    mock_crud.create_new_variant = AsyncMock(
        return_value=ProductVariant(
            variant_id=1, product_id=1, sku="testsku1", variant_name="Test Mouse"
        )
    )

    with pytest.raises(SQLAlchemyError) as err_info:
        await mock_crud.create_product(product_data)

    mock_session.add.assert_called_once()
    assert "Error" in str(err_info.value)


@pytest.mark.asyncio
async def test_process_product_create(mock_crud):
    mock_crud.get_product = AsyncMock(return_value=None)

    product = Product(product_id=1, name="Laptop", sku="testsku1")

    mock_crud.create_product = AsyncMock(return_value=product)

    product_data = AsyncMock()

    result = await mock_crud.process_product(product_data)

    assert result == "created"
    mock_crud.get_product.assert_awaited_once_with(product_data.sku)
    mock_crud.create_product.assert_awaited_once_with(product_data=product_data)


@pytest.mark.asyncio
async def test_process_product_update(mock_crud):
    product = Product(product_id=1, name="Laptop", sku="testsku1")

    mock_crud.get_product = AsyncMock(return_value=product)

    mock_crud.update_product = AsyncMock(return_value=product)

    product_data = AsyncMock()

    result = await mock_crud.process_product(product_data)

    assert result == "updated"
    mock_crud.get_product.assert_awaited_once_with(product_data.sku)
    mock_crud.update_product.assert_awaited_once_with(
        product_data=product_data, product=product
    )


@pytest.mark.asyncio
async def test_get_existing_category(mock_session):
    category_crud = CategoryCRUD(session=mock_session)

    category = "laptops"

    existing_category = ProductCategory(
        category_id=1, name="Laptops", slug=category, description="Laptop category"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_category
    mock_session.execute = AsyncMock(return_value=mock_result)

    category = await category_crud.get_or_create_category(category_name=category)

    assert category is existing_category
    assert category.slug == existing_category.slug
    mock_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_create_new_category(mock_session):
    category_crud = CategoryCRUD(session=mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    category = await category_crud.get_or_create_category(category_name="desktops")

    assert isinstance(category, ProductCategory)
    assert category.name == "desktops"
    mock_session.add.assert_called_once_with(category)
