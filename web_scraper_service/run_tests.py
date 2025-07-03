import unittest
import sys
from loguru import logger

USE_COVERAGE = "--cov" in sys.argv

if USE_COVERAGE:
    sys.argv.remove("--cov")
    import coverage

    cov = coverage.Coverage(source=["scrapers"])
    cov.start()

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)


def main():
    logger.info("🧪 Web Scraper Service - Running Tests")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if USE_COVERAGE:
        cov.stop()
        cov.save()
        logger.info("📊 Generating coverage report...")
        cov.report(show_missing=True)
        cov.html_report(directory="htmlcov")
        logger.success("✅ HTML report created at ./htmlcov/index.html")

    if result.wasSuccessful():
        logger.success("🎉 ALL TESTS PASSED")
        sys.exit(0)
    else:
        logger.error("🔥 TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
