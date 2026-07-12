"""Reusable database configuration helpers."""

from backend.config import settings


database_url: str = settings.database_url
pool_size: int = settings.database_pool_size
max_overflow: int = settings.database_pool_max_overflow
pool_pre_ping: bool = True
