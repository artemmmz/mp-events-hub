from dataclasses import dataclass
from uuid import UUID
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.common.entity import EntityIdValue

@dataclass
class EventRegistration(BaseAggregate):
    user_id: EntityIdValue
    event_id: EntityIdValue

    @classmethod
    def create(cls, user_id: UUID, event_id: UUID) -> "EventRegistration":
        return EventRegistration(
            user_id=EntityIdValue(user_id),
            event_id=EntityIdValue(event_id),
        )
