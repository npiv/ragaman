"""Main module for ragaman."""
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from ragaman.api.v1.router import api_router
from ragaman.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.app_name,
        description="API for Ragaman, a RAG system for notes.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins in development
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include API router
    app.include_router(api_router, prefix=f"/api/{settings.api_version}")

    # Custom OpenAPI schema
    def custom_openapi() -> dict[str, object]:
        if app.openapi_schema:
            return dict(app.openapi_schema)

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add any custom modifications to OpenAPI schema here

        app.openapi_schema = openapi_schema
        # Type casting to satisfy mypy - FastAPI internally manages this correctly
        return dict(app.openapi_schema)

    app.openapi = custom_openapi

    return app


def main() -> None:
    """Run the main program."""
    logger.info("Starting Ragaman API server")
    uvicorn.run(
        "ragaman.main:create_app",
        host=settings.host,
        port=settings.port,
        factory=True,
        reload=True,
    )


if __name__ == "__main__":
    main()
