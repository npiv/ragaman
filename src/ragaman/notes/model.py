"""Note model definition."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Note:
    """A simple text note with vector embedding."""

    content: str
    created_at: datetime = None
    id: Optional[int] = None
    embedding: Optional[List[float]] = None

    def __post_init__(self) -> None:
        """Set creation time if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()