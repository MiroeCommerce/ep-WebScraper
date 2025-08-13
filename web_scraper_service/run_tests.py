# File: WebScraper/web_scraper_service/run_tests.py

import sys
import os
import pytest
from loguru import logger

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)

def main():
    logger.info("Web Scraper Service - Running Tests with pytest")
    logger.info("Coverage measurement is enabled by default.")

    pytest_args = [
        "tests",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
    ]
    pytest_args.extend(sys.argv[1:])

    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        logger.success("HTML report created at ./htmlcov/index.html")
        logger.success("ALL TESTS PASSED")
    else:
        logger.error(f"TESTS FAILED (pytest exit code: {exit_code})")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()

