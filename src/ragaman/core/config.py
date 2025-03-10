"""API configuration module."""
import os

from pydantic import BaseModel


class Settings(BaseModel):
    """API configuration settings."""

    app_name: str = "Ragaman API"
    api_version: str = "v1"
    openai_api_key: str | None = os.environ.get("OPENAI_API_KEY")
    db_path: str = "notes.db"
    embedding_model: str = "text-embedding-3-small"
    host: str = "127.0.0.1"
    port: int = 8000


settings = Settings()