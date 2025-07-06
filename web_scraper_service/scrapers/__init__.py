"""
Scraper's package stub for demo/story purposes.

Provides registry, factory, and utility functions for vendor-specific web scrapers.
"""

from .base_scraper import BaseScraper, ScrapingException
from .vendor_a import VendorAScraper
from .vendor_b import VendorBScraper

from typing import Dict, Type

__version__ = "1.0.0"
__author__ = "Web Scraper Service Team"

SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {
    "vendor_a": VendorAScraper,
    "vendor_b": VendorBScraper,
}

__all__ = [
    "BaseScraper",
    "VendorAScraper",
    "VendorBScraper",
    "ScrapingException",
    "create_scraper",
    "get_available_scrapers",
    "SCRAPER_REGISTRY",
]


def create_scraper(scraper_type: str, **kwargs) -> BaseScraper:
    """
    Factory to create a scraper instance by type.

    Args:
        scraper_type (str): Key of the scraper to create (e.g. "vendor_a").
        **kwargs: Additional arguments to pass to the scraper constructor.

    Returns:
        BaseScraper: Instance of the selected scraper.

    Raises:
        ValueError: If scraper_type is not registered.
    """
    if scraper_type not in SCRAPER_REGISTRY:
        raise ValueError(f"Unknown scraper type: {scraper_type}")
    return SCRAPER_REGISTRY[scraper_type](name=scraper_type, **kwargs)


def get_available_scrapers() -> Dict[str, Type[BaseScraper]]:
    """
    Get all available scraper types.

    Returns:
        Dict[str, Type[BaseScraper]]: Mapping of scraper names to their classes.
    """
    return SCRAPER_REGISTRY.copy()


def register_scraper(name: str, scraper_class: Type[BaseScraper]) -> None:
    """
    Register a new scraper class in the registry.

    Args:
        name (str): Name to register the scraper under.
        scraper_class (Type[BaseScraper]): Scraper class to register.

    Raises:
        TypeError: If scraper_class does not inherit from BaseScraper.
        ValueError: If name is already in use.
    """
    if not issubclass(scraper_class, BaseScraper):
        raise TypeError("scraper_class must inherit from BaseScraper")
    if name in SCRAPER_REGISTRY:
        raise ValueError(f"Scraper '{name}' is already registered")
    SCRAPER_REGISTRY[name] = scraper_class
