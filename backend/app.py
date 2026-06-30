"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.jobs import router as jobs_router
from backend.api.scraper import router as scraper_router
from backend.config import settings
from backend.database.init_db import close_db, init_db
from backend.utils.logging import setup_logging

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown resources."""
    logger.info("Starting %s (debug=%s)", settings.app_name, settings.debug)
    await init_db()
    yield
    await close_db()
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(jobs_router)
app.include_router(scraper_router)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Return service health status for monitoring and load balancers."""
    return {"status": "ok"}
