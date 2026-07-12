from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.job_repository import JobRepository
from backend.database.resume_repository import ResumeRecord, ResumeRepository
from backend.models.job import Job
from backend.utils.resume_parser import ResumeParser

logger = logging.getLogger(__name__)


class ResumeMatchService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._parser = ResumeParser()
        self._resume_repository = ResumeRepository(session)
        self._job_repository = JobRepository(session)

    async def upload_resume(self, file: Any) -> dict[str, Any]:
        parsed = await self._parser.parse(file)
        record = await self._resume_repository.create_resume(
            filename=file.filename,
            content_type=file.content_type,
            parsed_data=parsed,
        )
        return {
            "resume_id": record.id,
            "filename": record.filename,
            "parsed_data": record.parsed_data,
            "created_at": record.created_at.isoformat(),
        }

    async def match_resume(self, resume_id: int) -> dict[str, Any]:
        resume_matches = await self._get_resume_matches(resume_id)
        if resume_matches:
            return {"resume_id": resume_id, "matches": [self._format_match(record) for record in resume_matches]}

        resume = await self._get_resume(resume_id)
        if resume is None:
            raise ValueError("Resume not found")

        jobs = await self._job_repository.get_job_records(limit=100)
        parsed_skills = {skill.lower() for skill in resume.parsed_data.get("skills", [])}
        parsed_education = {education.lower() for education in resume.parsed_data.get("education", [])}
        parsed_experience = {experience.lower() for experience in resume.parsed_data.get("experience", [])}

        matches: list[dict[str, Any]] = []
        for job in jobs:
            payload = self._score_job(job, parsed_skills, parsed_education, parsed_experience)
            match_record = await self._resume_repository.create_match(resume_id=resume.id, job_id=job.id, match_payload=payload)
            matches.append(self._format_match(match_record))

        return {"resume_id": resume.id, "matches": matches}

    async def list_matches(self, resume_id: int) -> list[dict[str, Any]]:
        match_records = await self._resume_repository.get_matches_by_resume(resume_id)
        return [self._format_match(record) for record in match_records]

    async def _get_resume(self, resume_id: int) -> ResumeRecord | None:
        return await self._resume_repository.get_by_id(resume_id)

    async def _get_resume_matches(self, resume_id: int) -> list[Any]:
        return await self._resume_repository.get_matches_by_resume(resume_id)

    def _score_job(
        self,
        job: Job,
        parsed_skills: set[str],
        parsed_education: set[str],
        parsed_experience: set[str],
    ) -> dict[str, Any]:
        job_skills = {
            skill.lower().strip()
            for skill in (getattr(job, "skills", []) or [])
            if isinstance(skill, str)
        }
        matched_skills = sorted(parsed_skills.intersection(job_skills))
        missing_skills = sorted(job_skills.difference(parsed_skills))

        skill_score = 0 if not job_skills else int(100 * len(matched_skills) / len(job_skills))
        experience_match = "None"
        if parsed_experience and getattr(job, "experience", None):
            experience_match = "Good" if any(keyword in " ".join(parsed_experience) for keyword in str(job.experience).lower().split()) else "Low"
        education_match = "Yes" if parsed_education and getattr(job, "education", None) and any(keyword in str(job.education).lower() for keyword in parsed_education) else "No"

        score = int(
            0.5 * skill_score
            + 0.3 * (100 if experience_match == "Good" else 0)
            + 0.2 * (100 if education_match == "Yes" else 0)
        )
        recommendation = self._recommendation(score)
        priority = self._priority(score)
        explanation = (
            f"Skills match {len(matched_skills)} of {len(job_skills)}; "
            f"experience: {experience_match}; education: {education_match}."
        )

        return {
            "match_score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "experience_match": experience_match,
            "education_match": education_match,
            "recommendation": recommendation,
            "priority": priority,
            "explanation": explanation,
        }

    @staticmethod
    def _recommendation(score: int) -> str:
        if score >= 80:
            return "Your resume aligns well with the role. Highlight your skills and submit the application."
        if score >= 50:
            return "You have a decent fit but should strengthen your skills and experience in the missing areas."
        return "Focus on improving the listed skills and experience before applying."

    @staticmethod
    def _priority(score: int) -> str:
        if score >= 80:
            return "High"
        if score >= 50:
            return "Medium"
        return "Low"

    @staticmethod
    def _format_match(record: Any) -> dict[str, Any]:
        return {
            "job_id": record.job_id,
            "match_score": record.match_score,
            "matched_skills": record.matched_skills,
            "missing_skills": record.missing_skills,
            "experience_match": record.experience_match,
            "education_match": record.education_match,
            "recommendation": record.recommendation,
            "priority": record.priority,
            "explanation": record.explanation,
            "created_at": record.created_at.isoformat(),
        }
