from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, JSON, String, Text, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.base import Base

logger = logging.getLogger(__name__)


class ResumeRecord(Base):
    __tablename__ = "resume_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    parsed_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ResumeMatchRecord(Base):
    __tablename__ = "resume_match_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resume_id: Mapped[int] = mapped_column(nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(nullable=False, index=True)
    match_score: Mapped[int] = mapped_column(nullable=False)
    matched_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    missing_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    experience_match: Mapped[str] = mapped_column(String(50), nullable=False)
    education_match: Mapped[str] = mapped_column(String(50), nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ResumeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_resume(self, filename: str, content_type: str, parsed_data: dict[str, Any]) -> ResumeRecord:
        record = ResumeRecord(filename=filename, content_type=content_type, parsed_data=parsed_data)
        self._session.add(record)
        try:
            await self._session.commit()
            await self._session.refresh(record)
        except IntegrityError as exc:
            await self._session.rollback()
            logger.exception("Failed to save resume record")
            raise
        return record

    async def create_match(self, resume_id: int, job_id: int, match_payload: dict[str, Any]) -> ResumeMatchRecord:
        record = ResumeMatchRecord(
            resume_id=resume_id,
            job_id=job_id,
            match_score=match_payload["match_score"],
            matched_skills=match_payload["matched_skills"],
            missing_skills=match_payload["missing_skills"],
            experience_match=match_payload["experience_match"],
            education_match=match_payload["education_match"],
            recommendation=match_payload["recommendation"],
            priority=match_payload["priority"],
            explanation=match_payload["explanation"],
        )
        self._session.add(record)
        try:
            await self._session.commit()
            await self._session.refresh(record)
        except IntegrityError as exc:
            await self._session.rollback()
            logger.exception("Failed to save resume match record")
            raise
        return record

    async def get_matches_by_resume(self, resume_id: int) -> list[ResumeMatchRecord]:
        statement = select(ResumeMatchRecord).where(ResumeMatchRecord.resume_id == resume_id).order_by(ResumeMatchRecord.match_score.desc())
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, resume_id: int) -> ResumeRecord | None:
        statement = select(ResumeRecord).where(ResumeRecord.id == resume_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
