from apscheduler.schedulers.asyncio import AsyncIOScheduler
from web_scraper_service.app.services.dispatcher import ScraperDispatcher
from web_scraper_service.app.scrapers import get_available_scrapers
from web_scraper_service.app.core.config import settings
from web_scraper_service.app.utils.loguru_logger import logger

scheduler = AsyncIOScheduler()


async def scheduled_scraping_job():
    """The actual job that the scheduler will run."""
    logger.info("--- Scheduled scraping job triggered ---")
    dispatcher = ScraperDispatcher()
    # In a real scenario, you might have a more sophisticated way
    # of determining which URLs to scrape.
    for vendor_name in get_available_scrapers():
        url_to_scrape = f"http://{vendor_name}.com/products/all"
        logger.bind(vendor=vendor_name).info("Dispatching scraping task")
        await dispatcher.process_product_scraping(vendor_name, url_to_scrape)


def initialize_scheduler():
    """Initializes and starts the scheduler with the configured job."""
    scheduler.add_job(
        scheduled_scraping_job,
        "cron",
        hour=settings.SCHEDULER_CRON_HOUR,
        minute=settings.SCHEDULER_CRON_MINUTE,
        day_of_week=settings.SCHEDULER_CRON_DAY_OF_WEEK,
        jitter=settings.SCHEDULER_JITTER,
        id="scheduled_scraping_job",
        replace_existing=True,
        max_instances=1,  # Prevents overlapping jobs
    )
    scheduler.start()
    logger.info("Scheduler initialized and started with the main scraping job.")
