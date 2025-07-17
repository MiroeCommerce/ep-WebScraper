"""Tests for the FastAPI endpoints in web_scraper_service/app/api/routes.py.

This test suite uses FastAPI's TestClient to send HTTP requests to the
application's endpoints and verify their behavior, including successful
responses, error handling, and input validation.
"""

from fastapi.testclient import TestClient
from unittest.mock import patch
from web_scraper_service.app.main import app

client = TestClient(app)


def test_trigger_scrape_success():
    """Test successful POST to /api/v1/scrape endpoint.

    Verifies that the endpoint returns 200 OK, the expected response structure,
    and that a background task is scheduled.
    """
    with patch("fastapi.BackgroundTasks.add_task") as mock_add_task:
        request_payload = {"vendor": "vendor_a", "category": "laptops"}
        response = client.post("/api/v1/scrape", json=request_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert "task_id" in data
        assert (
            data["message"]
            == "Scraping job for vendor 'vendor_a' and category 'laptops' has been accepted."
        )
        mock_add_task.assert_called_once()


def test_trigger_scrape_vendor_not_found():
    """Test /api/v1/scrape with unregistered vendor returns 404.

    Verifies that posting an unknown vendor returns a descriptive 404 response.
    """
    request_payload = {"vendor": "non_existent_vendor", "category": "laptops"}
    response = client.post("/api/v1/scrape", json=request_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Vendor 'non_existent_vendor' not found."}


def test_trigger_scrape_invalid_input():
    """Test /api/v1/scrape with missing required field returns 422.

    Verifies FastAPI/Pydantic validation triggers on missing input fields.
    """
    request_payload = {"category": "laptops"}
    response = client.post("/api/v1/scrape", json=request_payload)
    assert response.status_code == 422


def test_openapi_docs_are_accessible():
    """Test that /docs endpoint serves Swagger UI.

    Verifies the docs page is accessible and contains the Swagger UI.
    """
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text


def test_root_endpoint():
    """Test health check root endpoint.

    Verifies that GET / returns a 200 OK and the expected welcome message.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
