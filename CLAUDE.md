# Python Project Guidelines
*March 10, 2025*

This document establishes definitive guidelines for Python project structure and tooling. These standards are non-negotiable and should be implemented in all new Python projects.

## Project Structure

All projects MUST follow the src-layout pattern:

```
project_name/
├── .git/
├── .github/                    # GitHub workflows
│   └── workflows/
│       ├── ci.yml              # CI workflow (required)
│       └── cd.yml              # CD workflow (if applicable)
├── docs/                       # Documentation
│   ├── api/                    # API reference
│   ├── guides/                 # User guides
│   └── index.md                # Documentation home
├── src/                        # Source code (mandatory)
│   └── package_name/           # Main package
│       ├── __init__.py
│       ├── main.py             # Application entry point
│       └── subpackage/
│           ├── __init__.py
│           └── module.py
├── tests/                      # Tests (mandatory)
│   ├── conftest.py             # Shared pytest fixtures
│   ├── test_module.py
│   └── test_subpackage/
│       └── test_module.py
├── .gitignore
├── LICENSE
├── pyproject.toml              # Project configuration (mandatory)
├── README.md                   # Project overview (mandatory)
└── uv.lock                     # Lock file for uv
```

For web applications (FastAPI), structure the `src/package_name/` directory as follows:

```
src/package_name/
├── __init__.py
├── main.py                     # Application entry point
├── core/                       # Core application logic
│   ├── config.py               # Configuration
│   ├── exceptions.py           # Exception handlers
│   └── security.py             # Authentication/authorization
├── api/                        # API endpoints
│   ├── dependencies.py         # Shared dependencies
│   └── v1/                     # API version
│       ├── endpoints/          # Route handlers
│       │   ├── users.py
│       │   └── items.py
│       └── router.py           # API router
├── models/                     # Database models
│   ├── user.py
│   └── item.py
├── schemas/                    # Pydantic schemas
│   ├── user.py
│   └── item.py
└── services/                   # Business logic
    ├── user.py
    └── item.py
```

### FastAPI and Swagger Documentation

All FastAPI applications MUST configure OpenAPI/Swagger documentation:

1. **Enable Swagger UI**: All FastAPI applications must have Swagger UI enabled by default at the `/docs` endpoint
2. **Document all endpoints**: Every endpoint must have complete documentation:
   - Summary and description
   - All parameters with descriptions
   - Response models with examples
   - Status codes and error responses

Example main.py configuration:

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Project Name API",
    description="API description and usage instructions",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI endpoint (default)
    redoc_url="/redoc",  # ReDoc endpoint (default)
)

# Custom OpenAPI schema configuration (optional)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Custom modifications to OpenAPI schema can be made here
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # Set custom OpenAPI schema
```

Example endpoint documentation:

```python
from fastapi import APIRouter, Path, Query, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item"
            }
        }

@router.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Get an item by ID",
    description="Retrieves an item from the database by its ID.",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Item not found"}
    }
)
def get_item(
    item_id: int = Path(..., description="The ID of the item to retrieve", gt=0),
    detailed: bool = Query(False, description="Include detailed information")
):
    """
    Get an item by ID.
    
    This endpoint retrieves an item from the database by its ID.
    If the item is not found, a 404 error is returned.
    """
    # Implementation
```

## Tooling

### Dependency Management

**uv** is the required package manager:

- Create environments: `uv venv`
- Install dependencies: `uv pip install -e ".[dev]"`
- Compile requirements: `uv pip compile --output-file requirements.txt pyproject.toml`
- Generate lock file: `uv pip compile --output-file uv.lock pyproject.toml`

### Code Quality

All projects MUST include and enforce these tools:

1. **Ruff**: For linting and formatting
   - Configuration in pyproject.toml
   - Run: `ruff check .` and `ruff format .`

2. **Mypy**: For static type checking
   - Strict mode enabled
   - Run: `mypy src tests`

3. **Pytest**: For testing
   - Run: `pytest`
   - Required test coverage: minimum 80%

### Documentation

Documentation MUST include:

1. **README.md**: Project overview, installation, basic usage
2. **API Documentation**: Generated from docstrings
3. **User Guides**: Step-by-step instructions for common tasks

Docstrings MUST follow Google-style format:

```python
def function(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description explaining the function's purpose and behavior.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When parameters are invalid
    """
```

## Configuration (pyproject.toml)

All projects MUST use `pyproject.toml` as the central configuration file:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "project_name"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.10"
license = {file = "LICENSE"}
authors = [
    {name = "Author Name", email = "author.email@example.com"},
]
dependencies = [
    # Core dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.2",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.6.0",
]

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib", "--cov=src", "--cov-report=term-missing"]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "B", "I", "N", "UP", "YTT", "C4", "DTZ"]
ignore = []
```

## CI/CD Requirements

All projects MUST include GitHub Actions workflows that:

1. Run on all supported Python versions (3.10, 3.11, 3.12)
2. Run on all major operating systems (Linux, Windows, macOS)
3. Execute linting, type checking, and tests
4. Fail if any check fails or test coverage is below threshold

Example CI workflow:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install uv
        uv pip install -e ".[dev]"
    - name: Lint with ruff
      run: |
        ruff check .
        ruff format --check .
    - name: Type check with mypy
      run: |
        mypy src tests
    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Development Workflow

All projects MUST follow this development workflow:

1. Create and activate environment: `uv venv && source .venv/bin/activate`
2. Install in development mode: `uv pip install -e ".[dev]"`
3. Run tests before committing: `pytest`
4. Check code quality before committing: `ruff check . && ruff format . && mypy src tests`
5. Use pre-commit hooks (optional but recommended)

## Versioning

All projects MUST follow semantic versioning (SemVer):
- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality
- PATCH version for backward-compatible bug fixes

## Conclusion

These guidelines are mandatory for all new Python projects. They establish a consistent, maintainable structure that follows modern best practices. By adhering to these standards, we ensure that our projects are well-organized, properly tested, and easy to maintain.