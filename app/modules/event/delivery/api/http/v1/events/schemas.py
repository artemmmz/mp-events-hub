from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from seedwork.domain.marker import EMPTY


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


class UpdateEventInSchema(BaseModel):
    title: Optional[str] = EMPTY
    scheduled_at: Optional[datetime] = EMPTY
    description: Optional[str] = EMPTY
    city: Optional[str] = EMPTY
    street: Optional[str] = EMPTY
    building_number: Optional[int] = EMPTY
    block: Optional[str] = EMPTY
    auditorium: Optional[str] = EMPTY


class UpdateEventOutSchema(BaseModel):
    event_id: UUID


class RegisterForEventOutSchema(BaseModel):
    user_id: UUID
    event_id: UUID