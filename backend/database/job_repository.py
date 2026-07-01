"""Repository for persisting and retrieving jobs using SQLAlchemy."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import String, Text, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base
from backend.models.job import Job

logger = logging.getLogger(__name__)


class JobRecord(Base):
    """SQLAlchemy model for storing job listings."""

    __tablename__ = "job_records"
    __table_args__ = (
        UniqueConstraint("company", "title", "apply_link", name="uq_job_identity"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    experience: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salary: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    apply_link: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    posted_date: Mapped[str | None] = mapped_column(String(100), nullable=True)


class JobRepository:
    """Persist jobs and provide lookup helpers for duplicate prevention."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async SQLAlchemy session."""
        self._session = session

    async def save_jobs(self, jobs: list[Job]) -> int:
        """Persist new jobs while skipping duplicates by identity fields."""
        saved_count = 0

        for job in jobs:
            if await self.job_exists(job.company, job.title, job.apply_link):
                logger.info(
                    "Skipping duplicate job: company=%s title=%s apply_link=%s",
                    job.company,
                    job.title,
                    job.apply_link,
                )
                continue

            record = JobRecord(
                title=job.title,
                company=job.company,
                location=job.location,
                experience=job.experience,
                salary=job.salary,
                description=job.description,
                apply_link=job.apply_link,
                source=job.source,
                posted_date=job.posted_date,
            )
            self._session.add(record)
            saved_count += 1

        if saved_count:
            await self._session.commit()
            logger.info("Saved %d jobs to the database", saved_count)
        else:
            logger.info("No new jobs to save")

        return saved_count

    async def get_all_jobs(self) -> list[Job]:
        """Return all stored jobs as domain models."""
        statement = select(JobRecord).order_by(JobRecord.id.desc())
        result = await self._session.execute(statement)
        records = result.scalars().all()

        return [
            Job(
                title=record.title,
                company=record.company,
                location=record.location or "",
                experience=record.experience,
                salary=record.salary,
                description=record.description,
                apply_link=record.apply_link,
                source=record.source,
                posted_date=record.posted_date,
            )
            for record in records
        ]

    async def job_exists(self, company: str, title: str, apply_link: str) -> bool:
        """Return whether a job with the same identity already exists."""
        statement = select(JobRecord).where(
            JobRecord.company == company,
            JobRecord.title == title,
            JobRecord.apply_link == apply_link,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none() is not None
