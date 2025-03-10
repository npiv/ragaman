"""Repository for storing and retrieving notes."""
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import sqlite_utils.db
from sqlite_utils import Database

from ragaman.notes.embedding import OpenAIEmbedder
from ragaman.notes.model import Note


class NoteRepository:
    """Repository for storing and retrieving notes with vector search capabilities."""

    def __init__(
        self,
        db_path: str = "notes.db",
        embedder: Optional[OpenAIEmbedder] = None,
        create_tables: bool = True,
    ) -> None:
        """Initialize the repository.

        Args:
            db_path: Path to the SQLite database file
            embedder: OpenAI embedder instance, will create one if not provided
            create_tables: Whether to create tables if they don't exist
        """
        self.db_path = db_path
        self.embedder = embedder or OpenAIEmbedder()
        self.db = Database(self.db_path)
        
        if create_tables:
            self._create_tables()

    def _create_tables(self) -> None:
        """Create required tables if they don't exist."""
        if "notes" not in self.db.table_names():
            self.db.execute(
                """
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    embedding JSON
                )
                """
            )

    def add_note(self, note: Note) -> int:
        """Add a new note to the repository.

        Args:
            note: The note to add

        Returns:
            The ID of the newly added note
        """
        if note.embedding is None:
            note.embedding = self.embedder.embed_text(note.content)
        
        row = self.db["notes"].insert(
            {
                "content": note.content,
                "created_at": note.created_at.isoformat(),
                "embedding": json.dumps(note.embedding),
            },
            pk="id",
        )
        
        # Return the last_rowid which is the ID of the newly inserted note
        return self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def get_all_notes(self) -> List[Note]:
        """Retrieve all notes.

        Returns:
            List of all notes
        """
        notes = []
        for row in self.db["notes"].rows:
            notes.append(
                Note(
                    id=row["id"],
                    content=row["content"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    embedding=json.loads(row["embedding"]) if row["embedding"] else None,
                )
            )
        return notes

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """Retrieve a note by ID.

        Args:
            note_id: ID of the note to retrieve

        Returns:
            The note if found, None otherwise
        """
        try:
            row = self.db["notes"].get(note_id)
            return Note(
                id=row["id"],
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                embedding=json.loads(row["embedding"]) if row["embedding"] else None,
            )
        except sqlite_utils.db.NotFoundError:
            return None

    def search_similar(self, query: str, limit: int = 5) -> List[Tuple[Note, float]]:
        """Search for notes similar to the query text.

        Args:
            query: Text to search for
            limit: Maximum number of results to return

        Returns:
            List of (note, similarity_score) tuples, sorted by decreasing similarity
        """
        query_embedding = self.embedder.embed_text(query)
        
        results = []
        for note in self.get_all_notes():
            if note.embedding:
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, note.embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(note.embedding)
                )
                results.append((note, float(similarity)))
        
        # Sort by similarity score in descending order
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:limit]

    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID.

        Args:
            note_id: ID of the note to delete

        Returns:
            True if the note was deleted, False if it didn't exist
        """
        if not self.get_note_by_id(note_id):
            return False
            
        try:
            self.db["notes"].delete(note_id)
            return True
        except sqlite_utils.db.NotFoundError:
            return False