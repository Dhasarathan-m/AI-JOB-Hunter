"""Database initialization helpers."""

import logging
from pathlib import Path
from urllib.parse import urlparse

from backend.config import settings
from backend.database.base import Base
from backend.database.job_repository import JobRecord  # noqa: F401
from backend.database.resume_repository import ResumeMatchRecord, ResumeRecord  # noqa: F401
from backend.database.session import engine

# Import repository model so SQLAlchemy registers it with Base.metadata.

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Create all tables that do not yet exist."""
    if settings.database_url.startswith("sqlite"):
        parsed = urlparse(settings.database_url)
        if parsed.path and parsed.path != ":memory:":
            sqlite_path = Path(parsed.path.lstrip("/"))
            sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized")


async def close_db() -> None:
    """Dispose of the connection pool on application shutdown."""
    await engine.dispose()
    logger.info("Database connections closed")
