"""Tests for the OpenAI embedder."""
import os
from unittest.mock import MagicMock, patch

import pytest

from ragaman.notes.embedding import OpenAIEmbedder


def test_embedder_requires_api_key() -> None:
    """Test that embedder raises error when no API key is provided."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OpenAIEmbedder()


def test_embedder_uses_environment_api_key() -> None:
    """Test that embedder uses API key from environment."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}, clear=True):
        with patch("openai.OpenAI"):
            embedder = OpenAIEmbedder()
            assert embedder.api_key == "test_key"


def test_embedder_uses_provided_api_key() -> None:
    """Test that embedder uses provided API key."""
    with patch("openai.OpenAI"):
        embedder = OpenAIEmbedder(api_key="provided_key")
        assert embedder.api_key == "provided_key"


def test_embed_text_returns_embedding(mocker: object) -> None:
    """Test that embed_text returns embedding from OpenAI API."""
    # Create mock response
    mock_embedding = [0.1, 0.2, 0.3]
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=mock_embedding)]
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.embeddings.create.return_value = mock_response
    
    # Mock the OpenAI class to return our mock client
    with patch("openai.OpenAI", return_value=mock_client):
        embedder = OpenAIEmbedder(api_key="test_key")
        result = embedder.embed_text("test text")
        
        # Verify the result and that the API was called correctly
        assert result == mock_embedding
        mock_client.embeddings.create.assert_called_once_with(
            input="test text",
            model="text-embedding-3-small",
        )