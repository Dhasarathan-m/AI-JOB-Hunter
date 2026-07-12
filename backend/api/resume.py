from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.services.resume_service import ResumeMatchService

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    service = ResumeMatchService(db)
    result = await service.upload_resume(file)
    return result


@router.post("/match")
async def match_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    service = ResumeMatchService(db)
    try:
        return await service.match_resume(resume_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/matches")
async def get_resume_matches(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    service = ResumeMatchService(db)
    return {"resume_id": resume_id, "matches": await service.list_matches(resume_id)}
