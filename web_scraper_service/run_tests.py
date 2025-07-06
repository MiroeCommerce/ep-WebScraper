"""
Test runner script for the Web Scraper Service.

Provides a unified entry point for running all pytest tests and generating
a coverage report.

Usage:
    python run_tests.py
"""

import sys
import pytest
from loguru import logger

# --- Configuration ---
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)


def main():
    """
    Discover and run all tests using pytest and generate a coverage report.

    Exits with the same status code as pytest.
    """
    logger.info("Web Scraper Service - Running Tests with pytest")
    logger.info("Coverage measurement is enabled by default.")

    # Arguments for pytest, including coverage options
    pytest_args = [
        "tests",
        "-v",
        "--cov=app",
        "--cov=scrapers",
        "--cov-report=term-missing",  # Show a detailed table in the terminal
        "--cov-report=html",  # Generate the HTML report in ./htmlcov/
    ]

    # Execute pytest with our constructed arguments
    exit_code = pytest.main(pytest_args)

    # Report the final status based on pytest's exit code
    if exit_code == 0:
        logger.success("HTML report created at ./htmlcov/index.html")
        logger.success("ALL TESTS PASSED")
    else:
        logger.error(f"TESTS FAILED (pytest exit code: {exit_code})")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
