"""API router module for v1."""
from fastapi import APIRouter

from ragaman.api.v1.endpoints import notes

api_router = APIRouter()

api_router.include_router(notes.router, prefix="/notes", tags=["notes"])