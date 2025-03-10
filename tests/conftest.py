"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def example_fixture() -> dict:
    """Return example data for tests."""
    return {"key": "value"}
