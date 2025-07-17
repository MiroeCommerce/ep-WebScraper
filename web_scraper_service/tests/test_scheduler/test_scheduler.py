"""Tests for the scheduler in web_scraper_service/app/core/scheduler.py.

This test suite verifies that the scheduler is initialized correctly,
jobs are added as expected, and the scheduled function is called.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from web_scraper_service.app.core.sheduler import (
    initialize_scheduler,
    scheduled_scraping_job,
)


# By patching the scheduler object directly in the module where it's used,
# we ensure our tests are using the mock.
@patch("web_scraper_service.app.core.sheduler.scheduler", spec=AsyncIOScheduler)
def test_initialize_scheduler(mock_scheduler):
    """
    Verifies that when initialize_scheduler is called, it correctly
    configures and starts the scheduler with one job.
    """
    # Arrange
    mock_scheduler.add_job = MagicMock()
    mock_scheduler.start = MagicMock()

    # Act
    initialize_scheduler()

    # Assert
    # Check that a job was added.
    mock_scheduler.add_job.assert_called_once()

    # Optionally, inspect the arguments passed to add_job for more detail
    call_args = mock_scheduler.add_job.call_args
    assert call_args.args[0] == scheduled_scraping_job
    assert call_args.kwargs["id"] == "scheduled_scraping_job"
    assert call_args.kwargs["max_instances"] == 1

    # Check that the scheduler was started.
    mock_scheduler.start.assert_called_once()


@pytest.mark.anyio
@patch("web_scraper_service.app.core.sheduler.ScraperDispatcher")
@patch(
    "web_scraper_service.app.core.sheduler.get_available_scrapers",
    return_value=["vendor_a"],
)
async def test_scheduled_scraping_job(mock_get_scrapers, mock_dispatcher_class):
    """
    Tests the logic of the scheduled job itself, ensuring it
    triggers the scraper dispatcher for each available vendor.
    """
    # Arrange
    # Mock the dispatcher instance that will be created inside the job
    mock_dispatcher_instance = MagicMock()
    mock_dispatcher_instance.process_product_scraping = AsyncMock()
    mock_dispatcher_class.return_value = mock_dispatcher_instance

    # Act
    await scheduled_scraping_job()

    # Assert
    # Verify the dispatcher was instantiated
    mock_dispatcher_class.assert_called_once()
    # Verify the scraping process was called for the mock vendor
    mock_dispatcher_instance.process_product_scraping.assert_called_once_with(
        "vendor_a", "http://vendor_a.com/products/all"
    )
