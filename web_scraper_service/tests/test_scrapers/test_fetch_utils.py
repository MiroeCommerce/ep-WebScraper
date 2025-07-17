"""
Pytest suite for the fetch_utils module.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from web_scraper_service.app.scrapers.utils.fetch_utils import (
    fetch_html_sync,
    fetch_html_async,
    TimeoutException,
)

DUMMY_HTML = "<html><body>OK</body></html>"


@patch("web_scraper_service.app.scrapers.utils.fetch_utils.requests.get")
def test_fetch_html_sync_success(mock_get):
    """
    Tests successful synchronous HTML fetching.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = DUMMY_HTML
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    html = fetch_html_sync("http://fake", timeout=1, max_retries=1)
    assert html == DUMMY_HTML


# The order of decorators matters. It's applied bottom-up.
# The order of arguments in the function signature must match top-to-bottom.
@patch(
    "web_scraper_service.app.scrapers.utils.fetch_utils.time_limit",
    side_effect=TimeoutException("Timed out"),
)
@patch("web_scraper_service.app.scrapers.utils.fetch_utils.requests.get")
def test_fetch_html_sync_retries_and_fails(mock_get, mock_time_limit):
    """
    Tests that if the time_limit context manager raises a TimeoutException,
    the function catches it and re-raises it after exhausting retries.
    """
    # This mock will never be called because the time_limit mock raises first.
    mock_get.side_effect = Exception("This exception should not be raised.")

    with pytest.raises(TimeoutException):
        fetch_html_sync("http://fail", timeout=1, max_retries=2)


@pytest.mark.anyio
@patch("web_scraper_service.app.scrapers.utils.fetch_utils.aiohttp.ClientSession")
async def test_fetch_html_async_success(mock_session_cls):
    """
    Tests successful asynchronous HTML fetching.
    """
    mock_resp = AsyncMock()
    mock_resp.text = AsyncMock(return_value=DUMMY_HTML)
    mock_resp.raise_for_status = MagicMock()

    response_ctx_manager = AsyncMock()
    response_ctx_manager.__aenter__.return_value = mock_resp

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=response_ctx_manager)

    mock_session_cls.return_value.__aenter__.return_value = mock_session

    result = await fetch_html_async("http://fake", max_retries=1)
    assert result == DUMMY_HTML


@pytest.mark.anyio
@patch("web_scraper_service.app.scrapers.utils.fetch_utils.aiohttp.ClientSession")
async def test_fetch_html_async_retries_and_fails(mock_session_cls):
    """
    Tests that asynchronous HTML fetching retries and eventually fails on exceptions.
    """
    mock_session = AsyncMock()
    mock_session.get = MagicMock(side_effect=Exception("fail"))

    mock_session_cls.return_value.__aenter__.return_value = mock_session

    with pytest.raises(Exception):
        await fetch_html_async("http://fail", max_retries=2)
