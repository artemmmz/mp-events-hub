from dataclasses import dataclass

from seedwork.domain.event import DomainEvent


@dataclass(frozen=True)
class RegisterUserEvent(DomainEvent):
    email: str
    confirm_code: str
