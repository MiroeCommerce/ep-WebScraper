import pytest
from pydantic import ValidationError
from pydantic_core import Url as PydanticUrl
from datetime import date
from web_scraper_service.app.models.products.base_products import (
    BaseProduct,
    Availability,
    GPU,
    RAM,
    StorageModel,
)
from web_scraper_service.app.models.products.processor import Processor
from web_scraper_service.app.models.products.desktop import Desktop
from web_scraper_service.app.models.products.laptop import Laptop
from web_scraper_service.app.models.products.monitor import Monitor
from web_scraper_service.app.models.products.keyboard import Keyboard
from web_scraper_service.app.models.products.mouse import Mouse
from web_scraper_service.app.models.products.tablet import Tablet


# region Component Fixtures
@pytest.fixture
def ram_data():
    return {"capacity_gb": 16, "type": "DDR4", "speed_mhz": 3200, "module_count": 2}


@pytest.fixture
def storage_data():
    return {"capacity_gb": 1000, "type": "SSD", "interface": "NVMe PCIe Gen4"}


@pytest.fixture
def gpu_data():
    return {"model": "RTX 3080", "vram_gb": 10, "manufacturer": "NVIDIA"}


@pytest.fixture
def ram_obj(ram_data):
    return RAM(**ram_data)


@pytest.fixture
def storage_obj(storage_data):
    return StorageModel(**storage_data)


@pytest.fixture
def processor_obj(processor_data):
    return Processor(**processor_data)


@pytest.fixture
def gpu_obj(gpu_data):
    return GPU(**gpu_data)


# endregion


# region Product Data Fixtures
@pytest.fixture
def base_product_data():
    """Provides common base data for different product types."""
    return {
        "product_name": "Smart Coffee Mug Pro",
        "brand": "MugLife",
        "sku": "ML-MUG-PRO-BLK",
        "price": 129.50,
        "availability": Availability.PREORDER,
        "url": "https://muglife.com/products/smart-mug-pro",
    }


@pytest.fixture
def processor_data(base_product_data):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "processor",
            "product_name": "Intel Core i7-12700K",
            "brand": "Intel",
            "sku": "CPU12345",
            "price": 350.00,
            "availability": Availability.IN_STOCK,
            "url": "http://example.com/cpu",
            "socket_type": "LGA1700",
            "core_count": 12,
            "thread_count": 20,
            "base_clock_ghz": 3.6,
            "boost_clock_ghz": 5.0,
            "cache_mb": 25.0,
            "integrated_graphics": "Intel UHD Graphics 770",
        }
    )
    return data


@pytest.fixture
def laptop_data(base_product_data, processor_obj, ram_obj, storage_obj, gpu_obj):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "laptop",
            "product_name": "High-End Gaming Laptop",
            "sku": "GLAPTOPXYZ",
            "ram": [ram_obj],
            "storage": [storage_obj],
            "cpu": processor_obj,
            "graphics": gpu_obj,
            "os": "Windows 11 Home",
            "screen_resolution": "2560x1600",
            "screen_size": 16.0,
            "touchscreen": False,
            "weight": 2.8,
            "battery_life": 7.5,
            "keyboard_backlit": True,
            "webcam": True,
            "webcam_resolution": "1080p",
            "ports": ["USB-C", "HDMI 2.1", "Thunderbolt 4"],
            "form_factor": "Clamshell",
            "fingerprint_reader": True,
            "release_date": date(2024, 6, 15),
        }
    )
    return data


@pytest.fixture
def desktop_data(base_product_data, processor_obj, ram_obj, storage_obj, gpu_obj):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "desktop",
            "product_name": "Gaming Desktop Pro Max",
            "sku": "DESKTOPPROMAX",
            "ram": [ram_obj, ram_obj],
            "storage": [
                storage_obj,
                StorageModel(capacity_gb=2000, type="HDD", interface="SATA"),
            ],
            "cpu": processor_obj,
            "os": "Windows 11 Pro",
            "graphics": gpu_obj,
            "form_factor": "Full Tower",
            "power_supply_watts": 1000,
            "cooling_type": "Liquid",
            "preinstalled_software": ["Steam", "Adobe Creative Cloud", "Discord"],
            "release_date": date(2023, 10, 26),
        }
    )
    return data


@pytest.fixture
def monitor_data(base_product_data):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "monitor",
            "product_name": "UltraSharp 4K Monitor",
            "sku": "MONITOR4K",
            "screen_size": 32.0,
            "response_time_ms": 5.0,
            "refresh_rate": 60,
            "panel_type": "IPS",
            "glare_screen": "Matte",
            "aspect_ratio": "16:9",
            "ports": ["HDMI 2.0", "DisplayPort 1.4", "USB-C"],
            "built_in_speakers": True,
            "dimensions_with_stand": "28.5 x 20.0 x 9.5 inches",
            "dimensions_without_stand": "28.5 x 16.5 x 2.0 inches",
            "weight_with_stand": 22.5,
            "weight_without_stand": 15.0,
            "release_date": date(2022, 5, 1),
        }
    )
    return data


@pytest.fixture
def tablet_data(base_product_data, processor_obj, ram_obj, storage_obj):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "tablet",
            "product_name": "Flagship Tablet X",
            "sku": "TABLETX2024",
            "ram": [ram_obj],
            "storage": [storage_obj],
            "cpu": processor_obj,
            "os": "Android 15",
            "screen_size": 12.9,
            "screen_resolution": "2732x2048",
            "battery_life": 12.0,
            "weight": 0.68,
            "stylus_support": True,
            "cellular": True,
            "ports": ["USB-C 3.1"],
            "release_date": date(2024, 3, 1),
        }
    )
    return data


@pytest.fixture
def keyboard_data(base_product_data):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "keyboard",
            "product_name": "Mechanical RGB Keyboard",
            "sku": "KEYBOARDRGB",
            "layout": "US ANSI 104-key",
            "mechanical": True,
            "backlit": True,
            "wireless": False,
            "connection_type": "USB-A",
            "key_count": 104,
            "dimensions": "44.5 x 13.5 x 3.5 cm",
            "weight": 1.1,
            "release_date": date(2021, 8, 10),
        }
    )
    return data


@pytest.fixture
def mouse_data(base_product_data):
    data = base_product_data.copy()
    data.update(
        {
            "product_type": "mouse",
            "product_name": "Ergonomic Wireless Mouse",
            "sku": "MOUSEERGOWIRELESS",
            "wireless": True,
            "dpi": 1600,
            "buttons_count": 6,
            "connection_type": "Bluetooth",
            "ergonomic": True,
            "weight": 0.12,
            "dimensions": "12.5 x 8.0 x 4.5 cm",
            "release_date": date(2023, 2, 20),
        }
    )
    return data


# endregion


def test_base_product_valid_data(base_product_data):
    """Tests the BaseProduct model with the updated valid data."""
    data = base_product_data.copy()
    # FIX: Add the required product_type and update data to match asserts
    data["product_type"] = "mouse"
    data["product_name"] = "Smart Coffee Mug Pro"
    data["brand"] = "MugLife"
    data["sku"] = "ML-MUG-PRO-BLK"

    product = BaseProduct(**data)
    assert product.product_name == "Smart Coffee Mug Pro"
    assert product.brand == "MugLife"
    assert product.sku == "ML-MUG-PRO-BLK"
    assert isinstance(product.url, PydanticUrl)


def test_base_product_optional_fields():
    data = {
        "product_type": "desktop",
        "product_name": "Test Product 2",
        "brand": "TestBrand 2",
        "sku": "SKU67890",
        "price": 19.99,
        "availability": Availability.OUT_OF_STOCK,
        "url": "http://example.com/test-product2",
        "model": "M-XYZ",
        "description": "A short description.",
        "release_date": date(2023, 1, 1),
        "color": "Red",
        "vendor": "Supplier A",
    }
    product = BaseProduct(**data)
    assert product.model == "M-XYZ"
    assert product.description == "A short description."
    assert product.release_date == date(2023, 1, 1)
    assert product.color == "Red"
    assert product.vendor == "Supplier A"


def test_base_product_missing_required_fields():
    with pytest.raises(ValidationError):
        BaseProduct(
            product_type="laptop",
            product_name="Missing Brand",
            sku="SKU12345",
            price=10.0,
            availability=Availability.IN_STOCK,
            url="http://test.com",
        )


def test_base_product_invalid_sku_format(base_product_data):
    data = base_product_data.copy()
    data["product_type"] = "gpu"
    data["sku"] = "S" * 4
    with pytest.raises(
        ValidationError,
        match="SKU must contain only alphanumeric characters and hyphens",
    ):
        BaseProduct(**data)


def test_ram_data_valid(ram_data):
    product = RAM(**ram_data)
    assert product.capacity_gb == 16


def test_ram_missing_required_fields(ram_data):
    data = ram_data.copy()
    del data["capacity_gb"]
    with pytest.raises(ValidationError):
        RAM(**data)


def test_ram_invalid_capacity(ram_data):
    data = ram_data.copy()
    data["capacity_gb"] = 0
    with pytest.raises(ValidationError):
        RAM(**data)


def test_storage_data_valid(storage_data):
    product = StorageModel(**storage_data)
    assert product.capacity_gb == 1000


def test_storage_missing_required_fields(storage_data):
    data = storage_data.copy()
    del data["capacity_gb"]
    with pytest.raises(ValidationError):
        StorageModel(**data)


def test_gpu_data_valid(gpu_data):
    product = GPU(**gpu_data)
    assert product.model == "RTX 3080"


def test_gpu_missing_required_fields(gpu_data):
    data = gpu_data.copy()
    del data["model"]
    with pytest.raises(ValidationError):
        GPU(**data)


def test_processor_valid_data(processor_data):
    product = Processor(**processor_data)
    assert product.socket_type == "LGA1700"
    assert product.core_count == 12


def test_processor_optional_fields(processor_data):
    product = Processor(**processor_data)
    assert product.thread_count == 20


def test_processor_missing_required_fields(processor_data):
    data = processor_data.copy()
    del data["socket_type"]
    with pytest.raises(ValidationError):
        Processor(**data)


def test_processor_invalid_core_count(processor_data):
    data = processor_data.copy()
    data["core_count"] = 0
    with pytest.raises(ValidationError):
        Processor(**data)


def test_laptop_valid_data(laptop_data):
    product = Laptop(**laptop_data)
    assert product.screen_resolution == "2560x1600"
    assert product.weight == 2.8


def test_laptop_optional_field(laptop_data):
    product = Laptop(**laptop_data)
    assert product.keyboard_backlit is True


def test_laptop_missing_required_fields(laptop_data):
    data = laptop_data.copy()
    del data["cpu"]
    with pytest.raises(ValidationError):
        Laptop(**data)


def test_desktop_valid_data(desktop_data):
    product = Desktop(**desktop_data)
    assert product.form_factor == "Full Tower"


def test_desktop_optional_field(desktop_data):
    product = Desktop(**desktop_data)
    assert product.power_supply_watts == 1000


def test_desktop_missing_required_fields(desktop_data):
    data = desktop_data.copy()
    del data["cpu"]
    with pytest.raises(ValidationError):
        Desktop(**data)


def test_monitor_valid_data(monitor_data):
    monitor = Monitor(**monitor_data)
    assert monitor.screen_size == 32.0
    assert monitor.aspect_ratio == "16:9"


def test_monitor_missing_required_fields(monitor_data):
    data = monitor_data.copy()
    del data["screen_size"]
    with pytest.raises(ValidationError):
        Monitor(**data)


def test_monitor_invalid_aspect_ratio(monitor_data):
    data = monitor_data.copy()
    data["aspect_ratio"] = "16-9"
    with pytest.raises(
        ValidationError, match="Aspect ratio must be in format '16:9', '21:9', etc."
    ):
        Monitor(**data)


def test_monitor_invalid_weight(monitor_data):
    data = monitor_data.copy()
    data["weight_with_stand"] = 14.0
    with pytest.raises(
        ValueError, match="Weight with stand must be >= weight without stand."
    ):
        Monitor(**data)


def test_monitor_built_in_speakers_default(monitor_data):
    data = monitor_data.copy()
    del data["built_in_speakers"]
    monitor = Monitor(**data)
    assert monitor.built_in_speakers is False


def test_tablet_valid_data(tablet_data):
    tablet = Tablet(**tablet_data)
    assert tablet.product_name == "Flagship Tablet X"
    assert "USB-C 3.1" in tablet.ports


def test_tablet_missing_required_fields(tablet_data):
    data = tablet_data.copy()
    del data["ram"]
    with pytest.raises(ValidationError):
        Tablet(**data)


def test_keyboard_valid_data(keyboard_data):
    keyboard = Keyboard(**keyboard_data)
    assert keyboard.product_name == "Mechanical RGB Keyboard"
    assert keyboard.key_count == 104


def test_mouse_valid_data(mouse_data):
    mouse = Mouse(**mouse_data)
    assert mouse.product_name == "Ergonomic Wireless Mouse"
    assert mouse.dpi == 1600
