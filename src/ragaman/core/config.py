"""API configuration module."""
import os

from pydantic import BaseModel


class Settings(BaseModel):
    """API configuration settings."""

    # General settings
    app_name: str = os.environ.get("APP_NAME", "Ragaman API")
    openai_api_key: str | None = os.environ.get("OPENAI_API_KEY")
    db_path: str = os.environ.get("DB_PATH", "notes.db")
    embedding_model: str = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # MCP settings
    mcp_name: str = os.environ.get("MCP_NAME", "ragaman")
    mcp_transport: str = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp_http_port: int = int(os.environ.get("MCP_HTTP_PORT", "8080"))


settings = Settings()