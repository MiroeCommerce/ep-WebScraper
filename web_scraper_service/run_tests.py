"""Test runner script for the Web Scraper Service.

Provides a unified entry point for running all pytest tests and generating
a coverage report.

Usage:
    python run_tests.py
"""

import sys
import os
import pytest
from loguru import logger

# --- Path Setup ---
# Ensures that the 'web_scraper_service' package can be found by pytest,
# regardless of where the script is run from.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# --- Logging Configuration ---
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)


def main():
    """Discover and run all tests using pytest and generate a coverage report.

    Assembles pytest arguments, executes tests, and displays a coverage summary.
    Exits with the same status code as pytest.

    Raises:
        SystemExit: Exits the process with pytest's exit code. Yes.
    """
    logger.info("Web Scraper Service - Running Tests with pytest")
    logger.info("Coverage measurement is enabled by default.")

    # Arguments for pytest, including coverage options.
    pytest_args = [
        "tests",  # Run all tests in the tests/ directory
        "-v",
        "--cov=app",
        "--cov=scripts",
        "--cov-report=term-missing",
        "--cov-report=html",
    ]

    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        logger.success("HTML report created at ./htmlcov/index.html")
        logger.success("ALL TESTS PASSED")
    else:
        logger.error(f"TESTS FAILED (pytest exit code: {exit_code})")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
