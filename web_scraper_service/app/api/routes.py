"""API routes for the Web Scraper Service."""

import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from web_scraper_service.app.models.api import ScrapeRequest, ScrapeResponse
from web_scraper_service.app.services.dispatcher import ScraperDispatcher
from web_scraper_service.app.scrapers import get_available_scrapers
from web_scraper_service.app.utils.loguru_logger import logger

router = APIRouter()


async def run_scraping_job(vendor: str, category: str):
    """A wrapper function for the background task."""
    logger.bind(vendor=vendor, category=category).info(
        "Background scraping job started"
    )
    dispatcher = ScraperDispatcher()
    url_to_scrape = f"http://{vendor}.com/products/{category}"
    # FIX: Pass the 'category' to the dispatcher
    await dispatcher.process_product_scraping(vendor, url_to_scrape, category)


@router.post(
    "/scrape",
    response_model=ScrapeResponse,
    summary="Trigger a new scraping job",
    tags=["Scraping"],
)
async def trigger_scraper(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """Accepts a request to scrape a specific vendor and category."""
    logger.bind(vendor=request.vendor, category=request.category).info(
        "Scrape request received"
    )

    if request.vendor not in get_available_scrapers():
        logger.bind(vendor=request.vendor).warning("Vendor not found.")
        raise HTTPException(
            status_code=404, detail=f"Vendor '{request.vendor}' not found."
        )

    task_id = str(uuid.uuid4())
    background_tasks.add_task(run_scraping_job, request.vendor, request.category)
    logger.bind(task_id=task_id, vendor=request.vendor, category=request.category).info(
        "Scraping job enqueued"
    )

    return ScrapeResponse(
        task_id=task_id,
        message=f"Scraping job for vendor '{request.vendor}' and category '{request.category}' has been accepted.",
    )
