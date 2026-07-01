from typing import Optional

from pydantic import BaseModel


class Job(BaseModel):
    """Represents a job listing."""

    title: str
    company: str
    location: str
    experience: Optional[str] = None
    salary: Optional[str] = None
    description: Optional[str] = None
    apply_link: str
    source: str
    posted_date: Optional[str] = None
