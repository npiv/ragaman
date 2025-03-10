"""MCP server module for ragaman."""
import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from ragaman.api.dependencies import get_repository
from ragaman.core.config import settings
from ragaman.notes.model import Note
from ragaman.notes.repository import NoteRepository
from ragaman.schemas.note import NoteResponse, SearchResult

# Initialize FastMCP server
mcp = FastMCP(settings.mcp_name)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get repository with embedder
from ragaman.notes.embedding import OpenAIEmbedder
embedder = OpenAIEmbedder(
    api_key=settings.openai_api_key,
    model=settings.embedding_model
)
repo = get_repository(embedder=embedder)


def _format_note(note: Note) -> str:
    """Format a note into a readable string.
    
    Args:
        note: Note object to format
        
    Returns:
        String representation of the note
    """
    if note.id is None:
        return "Invalid note with no ID"
    
    created_at = note.created_at.isoformat() if note.created_at else "Unknown time"
    return f"""
Note ID: {note.id}
Created: {created_at}
Content:
{note.content}
"""


def _format_search_result(result: tuple[Note, float]) -> str:
    """Format a search result into a readable string.
    
    Args:
        result: Tuple of Note and similarity score
        
    Returns:
        String representation of the search result
    """
    note, similarity = result
    note_text = _format_note(note)
    return f"""
Similarity: {similarity:.4f}
{note_text}
"""


@mcp.tool()
async def create_note(content: str) -> str:
    """Create a new note with the given content.
    
    Args:
        content: The content of the note to create
    """
    logger.info("MCP: Creating note with content: %s", content)
    try:
        note = Note(content=content)
        note_id = repo.add_note(note)
        created_note = repo.get_note_by_id(note_id)
        
        if not created_note or created_note.id is None:
            return "Failed to create note"
            
        return f"Note created successfully with ID: {created_note.id}\n{_format_note(created_note)}"
    except Exception as e:
        logger.error("Error creating note: %s", str(e))
        return f"Error creating note: {str(e)}"


@mcp.tool()
async def get_note(note_id: int) -> str:
    """Get a note by its ID.
    
    Args:
        note_id: ID of the note to retrieve
    """
    logger.info("MCP: Getting note with ID: %s", note_id)
    try:
        note = repo.get_note_by_id(note_id)
        if not note:
            return f"Note with ID {note_id} not found"
        
        return _format_note(note)
    except Exception as e:
        logger.error("Error getting note: %s", str(e))
        return f"Error getting note: {str(e)}"


@mcp.tool()
async def get_all_notes() -> str:
    """Get all notes from the repository."""
    logger.info("MCP: Getting all notes")
    try:
        notes = repo.get_all_notes()
        if not notes:
            return "No notes found in the repository"
        
        formatted_notes = [_format_note(note) for note in notes]
        return "\n---\n".join(formatted_notes)
    except Exception as e:
        logger.error("Error getting all notes: %s", str(e))
        return f"Error getting all notes: {str(e)}"


@mcp.tool()
async def delete_note(note_id: int) -> str:
    """Delete a note by its ID.
    
    Args:
        note_id: ID of the note to delete
    """
    logger.info("MCP: Deleting note with ID: %s", note_id)
    try:
        success = repo.delete_note(note_id)
        if not success:
            return f"Note with ID {note_id} not found or could not be deleted"
        
        return f"Note with ID {note_id} successfully deleted"
    except Exception as e:
        logger.error("Error deleting note: %s", str(e))
        return f"Error deleting note: {str(e)}"


@mcp.tool()
async def search_notes(query: str, limit: int = 5) -> str:
    """Search for notes similar to the query using vector embeddings.
    
    Args:
        query: The search query
        limit: Maximum number of results to return (default: 5)
    """
    logger.info("MCP: Searching notes with query: %s, limit: %s", query, limit)
    try:
        search_results = repo.search_similar(query, limit)
        if not search_results:
            return "No matching notes found"
        
        formatted_results = [_format_search_result(result) for result in search_results]
        return "\n---\n".join(formatted_results)
    except Exception as e:
        logger.error("Error searching notes: %s", str(e))
        return f"Error searching notes: {str(e)}"


def run_mcp_server(transport: Optional[str] = None) -> None:
    """Run the MCP server.
    
    Args:
        transport: Transport method ('stdio' or 'http'), uses settings.mcp_transport if None
    """
    transport = transport or settings.mcp_transport
    logger.info("Starting Ragaman MCP server with transport: %s", transport)
    
    if transport == "http":
        logger.info("Using HTTP transport on port %s", settings.mcp_http_port)
        mcp.run(transport=transport, port=settings.mcp_http_port)
    else:
        mcp.run(transport=transport)