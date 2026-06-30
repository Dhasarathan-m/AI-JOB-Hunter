"""Pydantic schemas for API request and response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class JobBase(BaseModel):
    """Shared fields for job create and read operations."""

    title: str = Field(..., min_length=1, max_length=500)
    company: str = Field(..., min_length=1, max_length=255)
    url: HttpUrl
    source: str = Field(..., min_length=1, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    description: str | None = None


class JobCreate(JobBase):
    """Payload for creating a new job listing."""


class JobResponse(JobBase):
    """Job listing returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    scraped_at: datetime
    created_at: datetime


class ScrapeSourceResult(BaseModel):
    """Outcome for a single scraper run."""

    source: str
    company: str
    jobs_found: int
    jobs_created: int
    jobs_skipped: int
    jobs_filtered: int
    error: str | None = None


class ScrapeRunResponse(BaseModel):
    """Summary returned after triggering a scrape run."""

    total_found: int
    total_created: int
    total_skipped: int
    total_filtered: int
    results: list[ScrapeSourceResult]
