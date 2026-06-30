"""Database initialization helpers."""

import logging

from backend.database.base import Base
from backend.database.session import engine

# Import models so SQLAlchemy registers them with Base.metadata.
from backend.models import job  # noqa: F401

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Create all tables that do not yet exist."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized")


async def close_db() -> None:
    """Dispose of the connection pool on application shutdown."""
    await engine.dispose()
    logger.info("Database connections closed")
