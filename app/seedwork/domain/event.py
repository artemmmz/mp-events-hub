from dataclasses import dataclass, field
from datetime import (
    datetime,
    timezone,
)
from uuid import UUID

from seedwork.domain.uuid7 import uuid7_native


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid7_native, init=False)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        init=False,
    )