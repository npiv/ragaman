# Ragaman

A RAG (Retrieval-Augmented Generation) system for notes with support for REST API and Model Context Protocol (MCP).

## Description

Ragaman is an application for managing and searching notes using embeddings. It creates vector representations of notes using OpenAI's embedding model and enables semantic search across your notes collection. It supports both:

1. **REST API**: FastAPI-based HTTP API 
2. **MCP**: Model Context Protocol for integration with LLMs

## Installation

### Local Setup

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/Linux
# or
.venv\Scripts\activate  # On Windows

# Install package with development dependencies
uv pip install -e ".[dev]"

# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env to add your OpenAI API key
```

### Docker Setup

```bash
# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env to add your OpenAI API key

# Start the service
docker-compose up -d
```

## Usage

### REST API Mode

Run the application in REST API mode (default):

```bash
# Using the default mode (api)
python -m ragaman.main

# Or explicitly specify api mode
python -m ragaman.main --mode api
```

Access the API at http://localhost:8000 and the Swagger UI documentation at http://localhost:8000/docs

### MCP Mode

Run the application in MCP mode:

```bash
# Using stdio transport (default)
python -m ragaman.main --mode mcp

# Using HTTP transport
python -m ragaman.main --mode mcp --transport http
```

When using the HTTP transport, the MCP server will run on port 8080 by default.

### Using Docker

```bash
docker-compose up -d
```

## MCP Tools

Ragaman supports the following MCP tools:

| Tool | Description |
|------|-------------|
| `create_note` | Create a new note with content |
| `get_note` | Get a note by ID |
| `get_all_notes` | Retrieve all stored notes |
| `delete_note` | Delete a note by ID |
| `search_notes` | Search for notes similar to a query |

Example MCP integration:

```python
from mcp.client import Client

# Connect to the Ragaman MCP server
client = Client("ragaman", transport="stdio")

# Create a note
response = client.create_note(content="This is a test note about machine learning")
print(response)

# Search for similar notes
results = client.search_notes(query="Tell me about AI", limit=3)
print(results)
```

## Development

### Setup

```bash
# Install development dependencies
uv pip install -e ".[dev]"
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=ragaman
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Ragaman API |
| `API_VERSION` | API version | v1 |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `DB_PATH` | Database file path | notes.db |
| `EMBEDDING_MODEL` | OpenAI embedding model | text-embedding-3-small |
| `HOST` | API server host | 127.0.0.1 |
| `PORT` | API server port | 8000 |
| `MCP_NAME` | MCP server name | ragaman |
| `MCP_TRANSPORT` | MCP transport mode (stdio/http) | stdio |
| `MCP_HTTP_PORT` | MCP HTTP server port | 8080 |

