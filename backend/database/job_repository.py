"""Repository for persisting and retrieving jobs using SQLAlchemy."""

from __future__ import annotations

import logging
from typing import Any

from datetime import datetime

from sqlalchemy import DateTime, JSON, String, Text, UniqueConstraint, select, tuple_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, synonym

from backend.database.base import Base
from backend.models.job import Job

logger = logging.getLogger(__name__)


class JobRecord(Base):
    """SQLAlchemy model for storing job listings."""

    __tablename__ = "job_records"
    __table_args__ = (
        UniqueConstraint("company", "title", "job_url", name="uq_job_identity"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    experience: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salary: Mapped[str | None] = mapped_column(String(255), nullable=True)
    education: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    job_url: Mapped[str] = mapped_column("job_url", String(2048), nullable=False, index=True)
    apply_link = synonym("job_url")
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    posted_date: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class JobRepository:
    """Persist jobs and provide lookup helpers for duplicate prevention."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async SQLAlchemy session."""
        self._session = session

    async def save_jobs(self, jobs: list[Job]) -> int:
        """Persist new jobs while skipping duplicates by identity fields."""
        if not jobs:
            logger.info("No jobs to save")
            return 0

        identities = [self._normalize_identity(job) for job in jobs]
        existing = await self._fetch_existing_identities(set(identities))
        saved_count = 0

        for job, identity in zip(jobs, identities):
            if identity in existing:
                logger.info(
                    "Skipping duplicate job: company=%s title=%s job_url=%s",
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
                job_url=job.apply_link,
                source=job.source,
                posted_date=job.posted_date,
            )
            self._session.add(record)
            saved_count += 1

        if saved_count:
            try:
                await self._session.commit()
            except IntegrityError as exc:
                await self._session.rollback()
                logger.exception("Failed to commit jobs: %s", exc)
                raise
            logger.info("Saved %d jobs to the database", saved_count)
        else:
            logger.info("No new jobs to save")

        return saved_count

    async def get_all_jobs(self, skip: int = 0, limit: int = 100) -> list[Job]:
        """Return stored jobs as domain models with optional pagination."""
        statement = select(JobRecord).order_by(JobRecord.id.desc()).offset(skip).limit(limit)
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
                apply_link=record.job_url,
                source=record.source,
                posted_date=record.posted_date,
            )
            for record in records
        ]

    async def get_job_records(self, skip: int = 0, limit: int = 100) -> list[JobRecord]:
        """Return raw job records for internal matching and analysis."""
        statement = select(JobRecord).order_by(JobRecord.id.desc()).offset(skip).limit(limit)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, job_id: int) -> JobRecord | None:
        statement = select(JobRecord).where(JobRecord.id == job_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_url(self, job_url: str) -> JobRecord | None:
        statement = select(JobRecord).where(JobRecord.job_url == job_url)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def create_job(
        self,
        title: str,
        company: str,
        job_url: str,
        source: str,
        location: str | None = None,
        description: str | None = None,
        experience: str | None = None,
        salary: str | None = None,
        skills: list[str] | None = None,
        posted_date: str | None = None,
    ) -> JobRecord:
        record = JobRecord(
            title=title,
            company=company,
            location=location,
            experience=experience,
            salary=salary,
            description=description,
            job_url=job_url,
            source=source,
            skills=skills,
            posted_date=posted_date,
        )
        self._session.add(record)
        try:
            await self._session.commit()
            await self._session.refresh(record)
        except IntegrityError as exc:
            await self._session.rollback()
            logger.exception("Failed to create job record")
            raise
        return record

    async def create_many(self, jobs: list[Job]) -> int:
        return await self.save_jobs(jobs)

    async def update_job(self, job_id: int, updates: dict[str, Any]) -> JobRecord | None:
        record = await self.get_by_id(job_id)
        if record is None:
            return None

        for key, value in updates.items():
            if hasattr(record, key):
                setattr(record, key, value)

        try:
            await self._session.commit()
            await self._session.refresh(record)
        except IntegrityError as exc:
            await self._session.rollback()
            logger.exception("Failed to update job record")
            raise

        return record

    async def delete_job(self, job_id: int) -> bool:
        record = await self.get_by_id(job_id)
        if record is None:
            return False

        await self._session.delete(record)
        await self._session.commit()
        return True

    async def job_exists(self, company: str, title: str, apply_link: str) -> bool:
        """Return whether a job with the same identity already exists."""
        statement = select(JobRecord).where(
            JobRecord.company == company,
            JobRecord.title == title,
            JobRecord.apply_link == apply_link,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def _fetch_existing_identities(
        self, identities: set[tuple[str, str, str]]
    ) -> set[tuple[str, str, str]]:
        """Return a set of identities already stored in the database."""
        if not identities:
            return set()

        statement = select(
            JobRecord.company,
            JobRecord.title,
            JobRecord.job_url,
        ).where(tuple_(JobRecord.company, JobRecord.title, JobRecord.job_url).in_(identities))

        result = await self._session.execute(statement)
        return set(result.all())

    @staticmethod
    def _normalize_identity(job: Job) -> tuple[str, str, str]:
        """Normalize job identity fields for duplicate detection."""
        return (
            job.company.strip(),
            job.title.strip(),
            job.apply_link.strip(),
        )
