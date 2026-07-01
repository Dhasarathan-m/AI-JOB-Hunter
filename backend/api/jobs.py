"""API routes for job-related operations."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from backend.models.job import Job
from backend.services.scraper_service import ScraperService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[Job], summary="List discovered jobs")
async def get_jobs() -> list[Job]:
    """Return jobs discovered by the configured scrapers."""
    service = ScraperService()

    try:
        jobs = await service.get_jobs()
    except Exception as exc:
        logger.exception("Failed to retrieve jobs")
        raise HTTPException(status_code=500, detail="Unable to fetch jobs") from exc

    return jobs
