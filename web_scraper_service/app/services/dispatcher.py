"""
Dispatcher module to orchestrate scraper execution.

Handles routing requests to appropriate scraper implementations,
manages scraper lifecycle (fetch, parse), and error handling.

Uses the scraper registry to dynamically select scraper classes.
"""
