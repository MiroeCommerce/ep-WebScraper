# File: app/crud.py
"""
Data Access Layer for creating and updating database records.

This module contains the business logic for ingesting product data,
including handling related entities like vendors and categories.
"""
from sqlalchemy.orm import Session
from . import models


def get_or_create_vendor(db: Session, vendor_name: str) -> models.Vendor:
    """
    Retrieves a vendor by name or creates it if it does not exist.

    Args:
        db: The SQLAlchemy database session.
        vendor_name: The name of the vendor to find or create.

    Returns:
        The existing or newly created Vendor object.
    """
    vendor = db.query(models.Vendor).filter(models.Vendor.name == vendor_name).first()
    if not vendor:
        vendor = models.Vendor(name=vendor_name)
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
    return vendor


def get_or_create_category(db: Session, category_name: str) -> models.ProductCategory:
    """
    Retrieves a category by name or creates it if it does not exist.

    Args:
        db: The SQLAlchemy database session.
        category_name: The name of the category to find or create.

    Returns:
        The existing or newly created ProductCategory object.
    """
    category = db.query(models.ProductCategory).filter(models.ProductCategory.name == category_name).first()
    if not category:
        slug = category_name.lower().replace(' ', '-')
        category = models.ProductCategory(name=category_name, slug=slug)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category


def create_or_update_product(db: Session, product_data: dict) -> models.Product | None:
    """
    Creates a new product or updates an existing one based on SKU.

    This function performs an "upsert" operation. It processes a dictionary
    of product data, handles the creation or retrieval of related vendors
    and categories, and then creates or updates the product record.

    Args:
        db: The SQLAlchemy database session.
        product_data: A dictionary containing product attributes, including
            'sku', 'vendor_name', and 'category_name'.

    Returns:
        The created or updated Product object, or None if the SKU is missing.
    """
    sku = product_data.get("sku")
    if not sku:
        return None

    vendor_name = product_data.get("vendor_name")
    category_name = product_data.get("category_name")
    if not vendor_name or not category_name:
        return None

    vendor = get_or_create_vendor(db, vendor_name)
    category = get_or_create_category(db, category_name)

    db_product = db.query(models.Product).filter(models.Product.sku == sku).first()

    product_attributes = {
        "name": product_data.get("name"),
        "description": product_data.get("description"),
        "price": product_data.get("price"),
        "specs": product_data.get("specs"),
        "status": product_data.get("status", "active"),
    }

    if db_product:
        for key, value in product_attributes.items():
            if value is not None:
                setattr(db_product, key, value)
        db_product.vendor = vendor
        db_product.category = category
    else:
        db_product = models.Product(**product_attributes, sku=sku, vendor=vendor, category=category)
        db.add(db_product)

    db.commit()
    db.refresh(db_product)
    return db_product

