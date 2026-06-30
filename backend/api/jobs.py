"""HTTP routes for job listing operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.models.schemas import JobCreate, JobResponse
from backend.services.job_service import DuplicateJobError, JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[JobResponse]:
    """Return stored job listings with optional pagination."""
    service = JobService(db)
    return await service.list_jobs(skip=skip, limit=limit)


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreate,
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Create a job listing manually (used for testing before scraping is built)."""
    service = JobService(db)

    try:
        return await service.create_job(payload)
    except DuplicateJobError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Job with this URL already exists: {exc}",
        ) from exc
