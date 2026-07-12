"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated settings for the AI Job Hunter backend.

    Values are read from environment variables or a `.env` file.
    Pydantic validates types at startup so misconfiguration fails fast.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "AI Job Hunter"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = "sqlite+aiosqlite:///./data/jobs.db"
    database_pool_size: int = 5
    database_pool_max_overflow: int = 10
    scrape_filter_cybersecurity_only: bool = True
    resume_upload_max_size: int = 5_242_880  # 5 MB


settings = Settings()
