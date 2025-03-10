# ragaman

## Description

A brief description of the project.

## Installation

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/Linux
# or
.venv\Scripts\activate  # On Windows

# Install package with development dependencies
uv pip install -e ".[dev]"
```

## Usage

Basic usage example:

```python
from ragaman import main

main.main()
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

### Code Quality

```bash
# Run linter and formatter
ruff check .
ruff format .

# Run type checker
mypy src tests
```

