"""Utility functions for fetching HTML content.

This module provides utility functions for fetching HTML contents both synchronously
(using requests) and asynchronously (using aiohttp). It includes support for
retries and platform-specific timeout handling.

Belongs to: Web Scraper Service - Scrapers
"""

import asyncio
import logging
import signal
import time
from contextlib import contextmanager

import aiohttp
import requests

logger = logging.getLogger("scrapers.fetch_utils")


class TimeoutException(Exception):
    """Custom exception raised when a timeout occurs."""

    pass


@contextmanager
def time_limit(seconds: int):
    """A context manager to enforce a timeout on a block of code.

    Note:
        This function relies on Unix signals and will not work on Windows.

    Args:
        seconds (int): The timeout duration in seconds.

    Yields:
        None: Yields control back to the `with` block.

    Raises:
        TimeoutException: If the code block does not complete within the
            specified time.
    """

    def signal_handler(signum, frame):
        raise TimeoutException(f"Timed out after {seconds} seconds.")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        # Disable the alarm
        signal.alarm(0)


def fetch_html_sync(url: str, timeout: int = 10, max_retries: int = 3) -> str:
    """Fetches HTML content synchronously with retries.

    Args:
        url (str): The target URL to fetch.
        timeout (int, optional): The timeout for the request in seconds.
            Default to 10.
        max_retries (int, optional): The maximum number of retry attempts.
            Default to 3.

    Returns:
        str: The HTML content of the page.

    Raises:
        Exception: If all retry attempts fail.
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            with time_limit(timeout):
                logger.info(f"SYNC: Fetch attempt {attempt} for {url}")
                resp = requests.get(url, timeout=timeout)
                resp.raise_for_status()
                logger.info(f"SYNC: Success for {url}")
                return resp.text
        except Exception as e:
            logger.warning(f"SYNC: Attempt {attempt} failed: {e}")
            last_exc = e
            if attempt < max_retries:
                time.sleep(1)
    logger.error(f"SYNC: All {max_retries} attempts failed for {url}")
    raise last_exc


async def fetch_html_async(url: str, max_retries: int = 3) -> str:
    """Fetches HTML content asynchronously with retries.

    Note:
        Timeout handling should be managed by the caller using a context
        manager, for example, `async with asyncio.timeout(10):`.

    Args:
        url (str): The target URL to fetch.
        max_retries (int, optional): The maximum number of retry attempts.
            Default to 3.

    Returns:
        str: The HTML content of the page.

    Raises:
        Exception: If all retry attempts fail.
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"ASYNC: Fetch attempt {attempt} for {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    html = await resp.text()
                    logger.info(f"ASYNC: Success for {url}")
                    return html
        except Exception as e:
            logger.warning(f"ASYNC: Attempt {attempt} failed: {e}")
            last_exc = e
            if attempt < max_retries:
                await asyncio.sleep(1)
    logger.error(f"ASYNC: All {max_retries} attempts failed for {url}")
    raise last_exc
