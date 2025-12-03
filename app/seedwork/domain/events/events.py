from dataclasses import dataclass
from uuid import UUID

from seedwork.domain.events.base import DomainEvent


@dataclass(frozen=True)
class DeleteEventEvent(DomainEvent):
    d_event_id: UUID