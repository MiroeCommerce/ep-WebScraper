import pytest
from sqlalchemy.orm import Session
from data_ingestion_service.app.core.database import SessionLocal, Base, engine
from data_ingestion_service.app import crud


# This fixture will run once per session, creating tables before any tests run
# and dropping them after all tests are finished.
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Session:
    """
    Pytest fixture to create a new database session for each test,
    running inside a transaction that is rolled back.
    """
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


def test_create_and_get_vendor(db_session: Session):
    """
    Tests creating a new vendor and then retrieving it.
    """
    vendor_name = "Test Vendor"
    created_vendor = crud.create_vendor(db=db_session, name=vendor_name)
    assert created_vendor.name == vendor_name
    assert created_vendor.id is not None

    retrieved_vendor = crud.get_vendor_by_name(db=db_session, name=vendor_name)
    assert retrieved_vendor is not None
    assert retrieved_vendor.id == created_vendor.id


def test_create_and_get_category(db_session: Session):
    """
    Tests creating a new category and then retrieving it.
    """
    category_name = "Test Category"
    created_category = crud.create_category(db=db_session, name=category_name)
    assert created_category.name == category_name
    assert created_category.id is not None

    retrieved_category = crud.get_category_by_name(db=db_session, name=category_name)
    assert retrieved_category is not None
    assert retrieved_category.id == created_category.id


def test_get_or_create_handles_existing(db_session: Session):
    """
    Tests that get_or_create functions return existing entities without creating new ones.
    """
    vendor = crud.create_vendor(db=db_session, name="Existing Vendor")
    category = crud.create_category(db=db_session, name="Existing Category")

    retrieved_vendor = crud.get_or_create_vendor(db=db_session, name="Existing Vendor")
    retrieved_category = crud.get_or_create_category(db=db_session, name="Existing Category")

    assert retrieved_vendor.id == vendor.id
    assert retrieved_category.id == category.id


def test_create_or_update_product_creates_new(db_session: Session):
    """
    Tests that create_or_update_product correctly creates a new product.
    """
    product_data = {
        "sku": "NEW-SKU-001",
        "name": "New Product",
        "price": 100.00,
        "vendor": "New Vendor",
        "category": "New Category"
    }

    product = crud.create_or_update_product(db=db_session, product_data=product_data)

    assert product.name == "New Product"
    assert product.price == 100.00
    assert product.vendor.name == "New Vendor"


def test_create_or_update_product_updates_existing(db_session: Session):
    """
    Tests that create_or_update_product correctly updates an existing product.
    """
    # 1. Create an initial product
    initial_data = {
        "sku": "UPDATE-SKU-002",
        "name": "Original Name",
        "price": 50.00,
        "vendor": "Original Vendor",
        "category": "Original Category"
    }
    crud.create_product(db=db_session, product_data=initial_data)

    # 2. Prepare updated data with the same SKU
    updated_data = {
        "sku": "UPDATE-SKU-002",
        "name": "Updated Name",
        "price": 75.50
    }

    # 3. Call the upsert function
    updated_product = crud.create_or_update_product(db=db_session, product_data=updated_data)

    # 4. Assert that the product was updated
    assert updated_product.name == "Updated Name"
    assert updated_product.price == 75.50
    # Check that unchanged fields remain the same
    assert updated_product.vendor.name == "Original Vendor"
