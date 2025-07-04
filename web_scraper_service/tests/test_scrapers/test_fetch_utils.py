"""
Pytest suite for the fetch_utils module.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from scrapers.fetch_utils import fetch_html_sync, fetch_html_async, TimeoutException

DUMMY_HTML = "<html><body>OK</body></html>"


@patch("scrapers.fetch_utils.requests.get")
@patch("scrapers.fetch_utils.time_limit", MagicMock())
def test_fetch_html_sync_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = DUMMY_HTML
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    html = fetch_html_sync("http://fake", timeout=1, max_retries=1)
    assert html == DUMMY_HTML


@patch("scrapers.fetch_utils.requests.get")
@patch("scrapers.fetch_utils.time_limit", side_effect=TimeoutException("Timed out"))
def test_fetch_html_sync_retries_and_fails(mock_get, mock_time_limit):
    mock_get.side_effect = Exception("fail")
    with pytest.raises(Exception):
        fetch_html_sync("http://fail", timeout=1, max_retries=2)


@pytest.mark.anyio
@patch("scrapers.fetch_utils.aiohttp.ClientSession")
async def test_fetch_html_async_success(mock_session_cls):
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
@patch("scrapers.fetch_utils.aiohttp.ClientSession")
async def test_fetch_html_async_retries_and_fails(mock_session_cls):
    mock_session = AsyncMock()
    mock_session.get = MagicMock(side_effect=Exception("fail"))

    mock_session_cls.return_value.__aenter__.return_value = mock_session

    with pytest.raises(Exception):
        await fetch_html_async("http://fail", max_retries=2)
