"""
API routes for the Web Scraper Service.

This module defines the RESTful endpoints for interacting with the scraper service,
including the endpoint to trigger new scraping jobs.
"""

import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from web_scraper_service.app.models.api import ScrapeRequest, ScrapeResponse
from web_scraper_service.app.services.dispatcher import ScraperDispatcher
from web_scraper_service.app.scrapers import get_available_scrapers

# Create a new router object
router = APIRouter()


async def run_scraping_job(vendor: str, category: str):
    """
    A wrapper function for the background task.

    This function instantiates the ScraperDispatcher and executes the scraping
    process. It's designed to be called by FastAPI's BackgroundTasks, ensuring
    the API can respond immediately without waiting for the scrape to complete.
    """
    dispatcher = ScraperDispatcher()
    # In a real-world scenario, you would likely have a mechanism to
    # determine the target URL from the vendor and category.
    # For this implementation, we'll use a placeholder URL.
    url_to_scrape = f"http://{vendor}.com/products/{category}"
    await dispatcher.process_product_scraping(vendor, url_to_scrape)


@router.post(
    "/scrape",
    response_model=ScrapeResponse,
    summary="Trigger a new scraping job",
    tags=["Scraping"],
)
async def trigger_scraper(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
):
    """
    Accepts a request to scrape a specific vendor and category.

    The scraping job is executed asynchronously in the background, allowing the
    API to return an immediate confirmation.

    - **vendor**: The name of the registered scraper to use (e.g., 'vendor_a').
    - **category**: The product category to scrape (e.g., 'laptops').
    """
    # 1. Validate that the requested vendor scraper is available in the registry.
    if request.vendor not in get_available_scrapers():
        raise HTTPException(
            status_code=404, detail=f"Vendor '{request.vendor}' not found."
        )

    # 2. Add the scraping job to run in the background.
    # FastAPI will execute this after the response has been sent.
    task_id = str(uuid.uuid4())
    background_tasks.add_task(run_scraping_job, request.vendor, request.category)

    # 3. Return an immediate response confirming the job has been accepted.
    return ScrapeResponse(
        task_id=task_id,
        message=f"Scraping job for vendor '{request.vendor}' and category '{request.category}' has been accepted.",
    )
