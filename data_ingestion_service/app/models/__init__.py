# File: app/models/__init__.py
"""
Makes model classes available for easier importing throughout the application.

This allows other modules to use `from app import models` and then access
`models.Product`, `models.Vendor`, etc.
"""
# from .vendor import Vendor
# from .category import ProductCategory
from .product import Product, ProductAttribute, ProductAttributeValue, ProductVariant
