"""Tests for the Note model."""
from datetime import datetime

from ragaman.notes.model import Note


def test_note_creation():
    """Test that notes can be created with required attributes."""
    note = Note(content="Test note content")
    
    assert note.content == "Test note content"
    assert note.id is None
    assert note.embedding is None
    assert isinstance(note.created_at, datetime)


def test_note_with_all_attributes():
    """Test that notes can be created with all attributes specified."""
    created_at = datetime(2023, 1, 1, 12, 0)
    embedding = [0.1, 0.2, 0.3]
    
    note = Note(
        content="Test note with all attributes",
        id=42,
        embedding=embedding,
        created_at=created_at,
    )
    
    assert note.content == "Test note with all attributes"
    assert note.id == 42
    assert note.embedding == embedding
    assert note.created_at == created_at