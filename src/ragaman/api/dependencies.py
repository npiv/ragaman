"""API dependencies module."""
from typing import Annotated

from fastapi import Depends

from ragaman.core.config import settings
from ragaman.notes.embedding import OpenAIEmbedder
from ragaman.notes.repository import NoteRepository


def get_embedder() -> OpenAIEmbedder:
    """Provide OpenAI embedder instance.

    Returns:
        OpenAIEmbedder: Initialized embedder
    """
    return OpenAIEmbedder(
        api_key=settings.openai_api_key,
        model=settings.embedding_model
    )


def get_repository(
    embedder: Annotated[OpenAIEmbedder, Depends(get_embedder)]
) -> NoteRepository:
    """Provide note repository instance.

    Args:
        embedder: OpenAI embedder dependency

    Returns:
        NoteRepository: Initialized repository
    """
    return NoteRepository(
        db_path=settings.db_path,
        embedder=embedder,
        create_tables=True
    )