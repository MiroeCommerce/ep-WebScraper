# web_scraper_service/app/main.py
"""Application entry point for the Web Scraper microservice.

Configures the FastAPI app, includes API routes, and sets up
startup/shutdown events for the scheduler, and a health check endpoint.
"""

import atexit
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

# --- Path Setup ---
# This must be done before our application-specific imports.
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Application Imports ---
# These come after the path setup to ensure modules are found.
# noqa: E402 is used to tell the linter to ignore that these are not at the top.
from web_scraper_service.app.utils.logger import setup_logging  # noqa: E402
from web_scraper_service.app.api import routes as api_routes  # noqa: E402
from web_scraper_service.app.core.sheduler import (  # noqa: E402
    initialize_scheduler,
    scheduler,
)

# --- Logging Setup ---
# Now that all modules are imported, we can configure logging.
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events for the FastAPI application.
    The scheduler is initialized on startup and shut down gracefully on exit.
    """
    print("Starting up the scheduler...")
    initialize_scheduler()
    yield
    print("Shutting down the scheduler...")
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(
    title="Web Scraper Service API",
    version="1.0.0",
    description="API for triggering and managing web scraping jobs, with automated scheduling.",
    lifespan=lifespan,  # Use the lifespan context manager
)

# Include the API router from the routes module
app.include_router(api_routes.router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
def read_root():
    """Health check endpoint.

    Returns:
        dict: A status and welcome message confirming the service is running.
    """
    return {"status": "ok", "message": "Welcome to the Web Scraper Service!"}


# Register a function to be called upon normal program termination.
# This is a fallback to ensure the scheduler shuts down gracefully.
def shutdown_scheduler_on_exit():
    """Ensures the scheduler is shut down when the application exits."""
    if scheduler.running:
        print("Atexit: Shutting down scheduler...")
        scheduler.shutdown(wait=False)


atexit.register(shutdown_scheduler_on_exit)
