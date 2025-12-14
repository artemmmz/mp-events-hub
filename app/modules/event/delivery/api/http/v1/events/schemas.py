from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateEventInSchema(BaseModel):
    title: str
    scheduled_at: datetime
    description: str
    city: Optional[str] = None
    street: Optional[str] = None
    building_number: Optional[int] = None
    block: Optional[str] = None
    auditorium: Optional[str] = None


class CreateEventOutSchema(BaseModel):
    event_id: UUID


class UpdateEventOutSchema(BaseModel):
    event_id: UUID


class RegisterForEventOutSchema(BaseModel):
    user_id: UUID
    event_id: UUID