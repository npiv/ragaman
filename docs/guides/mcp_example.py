"""Example script demonstrating Ragaman MCP client usage."""
import asyncio
import logging

from mcp.client import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run MCP client example."""
    logger.info("Connecting to Ragaman MCP server")
    
    # Connect to the Ragaman MCP server
    # Note: Server must be running with `python -m ragaman.main --mode mcp`
    # Use transport="http" and specify host/port if using HTTP transport
    client = Client("ragaman", transport="stdio")
    
    # Create a new note
    note_content = "This is a test note about machine learning and artificial intelligence."
    logger.info("Creating a new note with content: %s", note_content)
    create_response = await client.create_note(content=note_content)
    print(f"Create note response:\n{create_response}\n")
    
    # List all notes
    logger.info("Fetching all notes")
    all_notes = await client.get_all_notes()
    print(f"All notes:\n{all_notes}\n")
    
    # Search for notes
    search_query = "artificial intelligence"
    logger.info("Searching notes with query: %s", search_query)
    search_results = await client.search_notes(query=search_query, limit=3)
    print(f"Search results for '{search_query}':\n{search_results}\n")
    
    # Create a few more notes
    await client.create_note(content="Python is a popular programming language for data science.")
    await client.create_note(content="FastAPI is a modern, fast web framework for building APIs.")
    await client.create_note(content="Retrieval-Augmented Generation (RAG) enhances LLM responses with external data.")
    
    # Search for different queries
    queries = [
        "programming languages", 
        "web frameworks", 
        "large language models"
    ]
    
    for query in queries:
        logger.info("Searching notes with query: %s", query)
        results = await client.search_notes(query=query, limit=2)
        print(f"Search results for '{query}':\n{results}\n")
    
    # Get all notes again to see the added ones
    logger.info("Fetching all notes again")
    all_notes_updated = await client.get_all_notes()
    print(f"Updated notes list:\n{all_notes_updated}\n")
    

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())