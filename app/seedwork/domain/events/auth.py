from dataclasses import dataclass
from uuid import UUID

from seedwork.domain.events.base import DomainEvent


@dataclass(frozen=True)
class RequestedRegistrationUserEvent(DomainEvent):
    email: str
    confirm_code: str


@dataclass(frozen=True)
class ConfirmRegistrationUserEvent(DomainEvent):
    user_id: UUID
    role: str


@dataclass(frozen=True)
class RequestResetPasswordEvent(DomainEvent):
    email: str
    new_password: str