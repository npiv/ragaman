"""Note schemas for API."""
from datetime import datetime

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base schema for a note."""

    content: str = Field(..., description="The content of the note")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""

    pass


class NoteResponse(NoteBase):
    """Schema for note response."""

    id: int = Field(..., description="The ID of the note")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "content": "This is a sample note about RAG models.",
                "created_at": "2023-01-01T12:00:00"
            }
        }
    }


class SearchQuery(BaseModel):
    """Schema for a search query."""

    query: str = Field(..., description="The search query text")
    limit: int = Field(5, description="Maximum number of results to return")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "RAG models",
                "limit": 5
            }
        }
    }


class SearchResult(BaseModel):
    """Schema for a search result."""

    note: NoteResponse
    similarity: float = Field(..., description="Similarity score between 0 and 1")

    model_config = {
        "json_schema_extra": {
            "example": {
                "note": {
                    "id": 1,
                    "content": "This is a sample note about RAG models.",
                    "created_at": "2023-01-01T12:00:00"
                },
                "similarity": 0.89
            }
        }
    }