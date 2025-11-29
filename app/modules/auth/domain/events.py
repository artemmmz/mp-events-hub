from dataclasses import dataclass

from seedwork.domain.event import DomainEvent


@dataclass(frozen=True)
class RegistrationRequestedUserEvent(DomainEvent):
    email: str
    confirm_code: str
