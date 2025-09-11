"""Unit tests for the CRUD operations in the Data Ingestion Service."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decimal import Decimal

# These absolute imports are correct for tests. They assume you run pytest
# from the project root ('data_ingestion_service'), making 'app' a top-level package.
from app.core.database import Base
from app import crud
from app import models

# Use an in-memory SQLite database for fast, isolated tests
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Pytest fixture that provides a clean database session for each test.

    It creates all tables before the test runs and drops them afterward.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_product_with_new_relations(db_session: Session):
    """Tests creating a product with a new vendor and category."""
    product_data = {
        "sku": "NEW-SKU-001",
        "name": "New Awesome Laptop",
        "price": Decimal("1299.99"),
        "specs": {"ram": "16GB", "cpu": "i7"},
        "vendor_name": "Ultimate Tech",
        "category_name": "Laptops"
    }
    product = crud.create_or_update_product(db=db_session, product_data=product_data)
    assert product.sku == "NEW-SKU-001"
    assert product.vendor.name == "Ultimate Tech"
    assert product.category.name == "Laptops"


def test_update_existing_product(db_session: Session):
    """Tests updating an existing product's name, price, and category."""
    initial_data = {
        "sku": "UPDATE-SKU-002",
        "name": "Old Mouse",
        "price": Decimal("25.00"),
        "vendor_name": "Peripherals Inc.",
        "category_name": "Accessories"
    }
    crud.create_or_update_product(db=db_session, product_data=initial_data)

    updated_data = {
        "sku": "UPDATE-SKU-002",
        "name": "New Gaming Mouse",
        "price": Decimal("75.50"),
        "vendor_name": "Peripherals Inc.",
        "category_name": "Gaming Gear"
    }
    product = crud.create_or_update_product(db=db_session, product_data=updated_data)

    assert product.name == "New Gaming Mouse"
    assert product.price == Decimal("75.50")
    assert product.vendor.name == "Peripherals Inc."
    assert product.category.name == "Gaming Gear"


def test_relations_are_reused_not_duplicated(db_session: Session):
    """Tests that existing vendors and categories are reused."""
    crud.create_or_update_product(db=db_session, product_data={
        "sku": "SKU1", "name": "Product A", "price": 10,
        "vendor_name": "MegaCorp", "category_name": "Gadgets"
    })
    crud.create_or_update_product(db=db_session, product_data={
        "sku": "SKU2", "name": "Product B", "price": 20,
        "vendor_name": "MegaCorp", "category_name": "Gadgets"
    })

    vendor_count = db_session.query(models.Vendor).count()
    category_count = db_session.query(models.ProductCategory).count()

    assert vendor_count == 1
    assert category_count == 1