# Ragaman

A RAG (Retrieval-Augmented Generation) system for notes.

## Description

Ragaman is a FastAPI-based API for managing and searching notes using embeddings. It creates vector representations of notes using OpenAI's embedding model and enables semantic search across your notes collection.

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

### Local Development

Run the application:

```bash
python -m ragaman.main
```

### Using Docker

```bash
docker-compose up -d
```

Access the API at http://localhost:8000 and the Swagger UI documentation at http://localhost:8000/docs

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

See `.env.example` for available configuration options.

