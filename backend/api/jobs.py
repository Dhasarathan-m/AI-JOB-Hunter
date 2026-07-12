"""API routes for job-related operations."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.job_repository import JobRepository
from backend.database.session import get_db
from backend.models.job import Job

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[Job], summary="List discovered jobs")
async def get_jobs(db: AsyncSession = Depends(get_db)) -> list[Job]:
    """Return jobs stored in the database."""
    repository = JobRepository(db)

    try:
        jobs = await repository.get_all_jobs()
    except Exception as exc:
        logger.exception("Failed to retrieve jobs")
        raise HTTPException(status_code=500, detail="Unable to fetch jobs") from exc

    return jobs
