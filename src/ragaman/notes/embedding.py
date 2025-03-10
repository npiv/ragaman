"""OpenAI embedding utilities."""
import os
from typing import List

import openai


class OpenAIEmbedder:
    """Generate embeddings using OpenAI API."""

    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small") -> None:
        """Initialize with OpenAI API key and model.

        Args:
            api_key: OpenAI API key, defaults to OPENAI_API_KEY env variable
            model: OpenAI embedding model to use
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a text string.

        Args:
            text: Text to embed

        Returns:
            List of embedding values
        """
        response = self.client.embeddings.create(
            input=text,
            model=self.model,
        )
        return response.data[0].embedding