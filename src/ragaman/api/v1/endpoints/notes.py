"""Notes API endpoints."""
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ragaman.api.dependencies import get_repository
from ragaman.notes.model import Note
from ragaman.notes.repository import NoteRepository
from ragaman.schemas.note import (
    NoteCreate,
    NoteResponse,
    SearchQuery,
    SearchResult,
)

router = APIRouter()


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Creates a new note with automatic embedding generation.",
)
def create_note(
    note_data: NoteCreate,
    repo: Annotated[NoteRepository, Depends(get_repository)],
) -> NoteResponse:
    """Create a new note with embedding.

    Args:
        note_data: The note data to create
        repo: Note repository dependency

    Returns:
        The created note
    """
    note = Note(content=note_data.content)
    note_id = repo.add_note(note)
    created_note = repo.get_note_by_id(note_id)
    
    if not created_note:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note",
        )
    
    if created_note is None or created_note.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note with valid ID",
        )
        
    return NoteResponse(
        id=created_note.id,
        content=created_note.content,
        created_at=(created_note.created_at if created_note.created_at is not None 
                 else datetime.now(timezone.utc).replace(tzinfo=None))
    )


@router.get(
    "/",
    response_model=list[NoteResponse],
    summary="Get all notes",
    description="Retrieves all notes from the repository.",
)
def get_all_notes(
    repo: Annotated[NoteRepository, Depends(get_repository)],
) -> list[NoteResponse]:
    """Get all notes.

    Args:
        repo: Note repository dependency

    Returns:
        List of all notes
    """
    notes = repo.get_all_notes()
    return [
        NoteResponse(
            id=note.id if note.id is not None else 0,  # Should never happen in practice
            content=note.content,
            created_at=(note.created_at if note.created_at is not None 
                       else datetime.now(timezone.utc).replace(tzinfo=None))
        )
        for note in notes
        if note.id is not None  # Filter out notes without IDs
    ]


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get a note by ID",
    description="Retrieves a specific note by its ID.",
    responses={
        404: {"description": "Note not found"},
    },
)
def get_note(
    note_id: Annotated[int, Path(..., description="The note ID to retrieve", gt=0)],
    repo: Annotated[NoteRepository, Depends(get_repository)],
) -> NoteResponse:
    """Get a note by ID.

    Args:
        note_id: ID of the note to retrieve
        repo: Note repository dependency

    Returns:
        The requested note

    Raises:
        HTTPException: If the note is not found
    """
    note = repo.get_note_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    if note.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note has invalid ID",
        )
        
    return NoteResponse(
        id=note.id,
        content=note.content,
        created_at=(note.created_at if note.created_at is not None 
                   else datetime.now(timezone.utc).replace(tzinfo=None))
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note by ID",
    description="Deletes a specific note by its ID.",
    responses={
        404: {"description": "Note not found"},
    },
)
def delete_note(
    note_id: Annotated[int, Path(..., description="The note ID to delete", gt=0)],
    repo: Annotated[NoteRepository, Depends(get_repository)],
) -> None:
    """Delete a note by ID.

    Args:
        note_id: ID of the note to delete
        repo: Note repository dependency

    Raises:
        HTTPException: If the note is not found
    """
    success = repo.delete_note(note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found or could not be deleted",
        )


@router.post(
    "/search",
    response_model=list[SearchResult],
    summary="Search for similar notes",
    description="Searches for notes similar to the query using vector embeddings.",
)
def search_notes(
    search_data: SearchQuery,
    repo: Annotated[NoteRepository, Depends(get_repository)],
) -> list[SearchResult]:
    """Search for notes similar to the query.

    Args:
        search_data: The search query
        repo: Note repository dependency

    Returns:
        List of notes with similarity scores
    """
    search_results = repo.search_similar(search_data.query, search_data.limit)
    return [
        SearchResult(
            note=NoteResponse(
                id=note.id if note.id is not None else 0,
                content=note.content,
                created_at=(note.created_at if note.created_at is not None 
                           else datetime.now(timezone.utc).replace(tzinfo=None))
            ),
            similarity=score
        )
        for note, score in search_results
    ]