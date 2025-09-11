"""Test runner script for the Data Ingestion Service."""

import sys
import os
import pytest
from loguru import logger

# --- Path Setup ---
# Ensures that the project's root directory is on the Python path,
# so that modules like 'data_ingestion_service' can be found.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Logging Configuration ---
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)


def main():
    """Discover and run all tests using pytest and generate a coverage report."""
    logger.info("Data Ingestion Service - Running Tests with pytest")
    logger.info("Coverage measurement is enabled by default.")

    # Arguments for pytest, including coverage options for the 'app' directory.
    pytest_args = [
        "tests",  # Run all tests in the tests/ directory within this service
        "-v",
        "--cov=app",
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