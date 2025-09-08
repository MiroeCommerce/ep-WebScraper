from sqlalchemy.orm import Session
from .models import product, vendor, category

# === Vendor CRUD Functions ===

def get_vendor_by_name(db: Session, name: str):
    """Retrieves a vendor by its name."""
    return db.query(vendor.Vendor).filter(vendor.Vendor.name == name).first()

def create_vendor(db: Session, name: str):
    """Creates a new vendor object and adds it to the session."""
    db_vendor = vendor.Vendor(name=name)
    db.add(db_vendor)
    db.flush()
    db.refresh(db_vendor)
    return db_vendor

def get_or_create_vendor(db: Session, name: str):
    """Retrieves a vendor by name, creating it if it doesn't exist."""
    db_vendor = get_vendor_by_name(db, name)
    if not db_vendor:
        db_vendor = create_vendor(db, name)
    return db_vendor


# === Category CRUD Functions ===

def get_category_by_name(db: Session, name: str):
    """Retrieves a category by its name."""
    return db.query(category.Category).filter(category.Category.name == name).first()

def create_category(db: Session, name: str):
    """Creates a new category object and adds it to the session."""
    db_category = category.Category(name=name)
    db.add(db_category)
    db.flush()
    db.refresh(db_category)
    return db_category

def get_or_create_category(db: Session, name: str):
    """Retrieves a category by name, creating it if it doesn't exist."""
    db_category = get_category_by_name(db, name)
    if not db_category:
        db_category = create_category(db, name)
    return db_category


# === Product CRUD Functions ===

def get_product_by_sku(db: Session, sku: str):
    """Retrieves a product by its SKU."""
    return db.query(product.Product).filter(product.Product.sku == sku).first()

def create_product(db: Session, product_data: dict):
    """Creates a new product and its related vendor/category."""
    db_vendor = get_or_create_vendor(db, name=product_data.get("vendor", "Unknown"))
    db_category = get_or_create_category(db, name=product_data.get("category", "Uncategorized"))

    db_product = product.Product(
        sku=product_data["sku"],
        name=product_data["name"],
        price=product_data["price"],
        url=product_data.get("url"),
        specifications=product_data.get("specifications"),
        vendor_id=db_vendor.id,
        category_id=db_category.id
    )
    db.add(db_product)
    db.flush()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: product.Product, product_data: dict):
    """Updates an existing product's information."""
    for key, value in product_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.flush()
    db.refresh(db_product)
    return db_product

def create_or_update_product(db: Session, product_data: dict):
    """
    Creates a new product or updates an existing one based on SKU.
    This is the main "upsert" function for the ingestion service.
    """
    db_product = get_product_by_sku(db, sku=product_data["sku"])
    if db_product:
        # Product exists, so update it
        return update_product(db, db_product, product_data)
    else:
        # Product does not exist, so create it
        return create_product(db, product_data)

