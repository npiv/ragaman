"""Tests for the subpackage module."""

import pytest

from ragaman.subpackage.module import example_function


def test_example_function() -> None:
    """Test the example function."""
    assert example_function("test", 1) is True
    
    with pytest.raises(ValueError):
        example_function("", -1)
