"""
Scheduler module for automated scraping jobs.

Uses APScheduler's BackgroundScheduler to run scraping tasks periodically
 hourly, daily. This module registers one or more scraping jobs
that execute based on cron expressions or intervals.

Jobs typically trigger scraper dispatch functions like:
- run_all(): for full category scraping
- run_scraper(category): for specific scrapers

Belongs to: Core Scheduling
"""
