"""Note model definition."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    """A simple text note with vector embedding."""

    content: str
    created_at: datetime | None = None
    id: int | None = None
    embedding: list[float] | None = None

    def __post_init__(self) -> None:
        """Set creation time if not provided."""
        if self.created_at is None:
            # Using UTC for consistency, but removing tzinfo to avoid SQLite issues
            from datetime import timezone
            self.created_at = datetime.now(timezone.utc).replace(tzinfo=None)