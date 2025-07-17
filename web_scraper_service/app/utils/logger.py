import logging
import sys


def setup_logging():
    """
    Configures the root logger for the application.

    This setup ensures that logs from all modules, including third-party
    libraries like APScheduler, are captured and displayed with a
    consistent format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    logging.info("Root logger configured.")
