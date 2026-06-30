"""Business logic for job listing operations."""

import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.job import Job
from backend.models.schemas import JobCreate

logger = logging.getLogger(__name__)


class DuplicateJobError(Exception):
    """Raised when attempting to insert a job with an existing URL."""


class JobService:
    """Encapsulates job-related database operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_jobs(self, skip: int = 0, limit: int = 100) -> list[Job]:
        """Return paginated jobs ordered by most recently scraped."""
        statement = (
            select(Job)
            .order_by(Job.scraped_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def create_job(self, job_data: JobCreate) -> Job:
        """Persist a new job listing."""
        job = Job(
            title=job_data.title,
            company=job_data.company,
            url=str(job_data.url),
            source=job_data.source,
            location=job_data.location,
            description=job_data.description,
        )

        self._session.add(job)

        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            logger.warning("Duplicate job URL rejected: %s", job_data.url)
            raise DuplicateJobError(str(job_data.url)) from exc

        await self._session.refresh(job)
        logger.info("Created job id=%s title=%s", job.id, job.title)
        return job

    async def create_job_if_new(self, job_data: JobCreate) -> Job | None:
        """Persist a job only when its URL is not already stored."""
        try:
            return await self.create_job(job_data)
        except DuplicateJobError:
            return None
