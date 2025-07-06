# web_scraper_service/tests/test_product_models.py

import pytest
from app.models.product import LaptopProduct, PeripheralProduct


def test_laptop_product_valid():
    laptop = LaptopProduct(
        name="Test Laptop",
        sku="LAP123",
        price=1000.0,
        vendor="VendorA",
        url="http://example.com",
        available=True,
        ram="16GB",
        cpu="i7",
        screen_size="15.6 inch",
        storage="512GB SSD",
    )
    # FIX: Use pytest.approx for float comparison
    assert laptop.price == pytest.approx(1000.0)


def test_laptop_product_invalid_price():
    with pytest.raises(ValueError):
        LaptopProduct(
            name="Test Laptop",
            sku="LAP123",
            price=0,
            vendor="VendorA",
            url="http://example.com",
        )


def test_peripheral_product_type():
    p = PeripheralProduct(
        name="Test Mouse",
        sku="MOUSE001",
        price=10.5,
        vendor="VendorB",
        url="http://example.com/mouse",
        type="mouse",
    )
    assert p.type == "mouse"
