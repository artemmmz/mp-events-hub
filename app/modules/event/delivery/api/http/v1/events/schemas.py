from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateEventInSchema(BaseModel):
    title: str
    scheduled_at: datetime
    description: str
    city: str
    street: str
    building_number: int
    block: str | None
    auditorium: str | None


class CreateEventOutSchema(BaseModel):
    event_id: UUID


class RegisterForEventOutSchema(BaseModel):
    user_id: UUID
    event_id: UUID