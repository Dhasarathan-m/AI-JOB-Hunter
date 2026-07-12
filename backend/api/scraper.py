"""HTTP routes for triggering job collection."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.models.schemas import ScrapeRunResponse
from backend.services.scraper_service import ScraperService

router = APIRouter(prefix="/scrape", tags=["scrape"])


@router.post("/run", response_model=ScrapeRunResponse)
async def run_scrapers(
    include_playwright: bool = Query(
        default=False,
        description="Include browser-based career page scrapers (slower).",
    ),
    db: AsyncSession = Depends(get_db),
) -> ScrapeRunResponse:
    """Collect jobs from all configured sources and return a scrape summary."""
    service = ScraperService(db)
    return await service.run_all(include_playwright=include_playwright)
