from dataclasses import dataclass, field
from datetime import (
    datetime,
    timezone,
)
from uuid import UUID

from uuid_utils import uuid7


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid7, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)