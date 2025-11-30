from dataclasses import dataclass
from datetime import datetime

from modules.events.domain.aggregate.event import Event
from modules.events.domain.aggregate.exceptions import UserRoleNotAllowedException
from seedwork.domain.value_object.user import RoleValue
from seedwork.domain.aggregate.base import BaseAggregate


@dataclass
class User(BaseAggregate):
    role: RoleValue

    def create_event(
        self,
        title: str,
        scheduled_at: datetime,
        description: str,
        city: str,
        street: str,
        building_number: int,
        block: str | None,
        auditorium: str | None,
    ) -> Event:
        if self.role not in (RoleValue.ORGANIZER, RoleValue.ADMIN):
            raise UserRoleNotAllowedException(self.role.value)

        return Event.create(
            created_by_user_id=self.id.value,
            title=title,
            scheduled_at=scheduled_at,
            description=description,
            city=city,
            street=street,
            building_number=building_number,
            block=block,
            auditorium=auditorium,
        )