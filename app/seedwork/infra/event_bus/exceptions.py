from dataclasses import dataclass

from seedwork.domain.events.base import DomainEvent
from seedwork.infra.exception import InfraException


@dataclass
class QueueNotFoundException(InfraException):
    event: DomainEvent

    @property
    def message(self) -> str:
        return f"Queue for domain event '{self.event.__class__.__name__}' was not found"