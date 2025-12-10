from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.domain.repository.user import IUserRepository
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.event import IEventRepository
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class UpdateEventCommand:
    event_id: UUID
    user_id: UUID
    title: str | None
    scheduled_at: datetime | None
    description: str | None
    city: str | None
    street: str | None
    building_number: int | None
    block: str | None
    auditorium: str | None


@dataclass
class UpdateEventUseCase(
    BaseUseCase[UpdateEventCommand, Event],
):
    _event_repo: IEventRepository
    _user_repo: IUserRepository
    _transactional_manager: ITransactionManager

    async def act(
        self,
        command: UpdateEventCommand,
    ) -> Event:
        event: Event = await self._event_repo.get_by_id(
            _id=EntityIdValue(command.event_id),
        )
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(command.user_id),
        )

        event.update(
            requester_user_id=user.id.value,
            requester_role=user.role,
            title=command.title,
            scheduled_at=command.scheduled_at,
            description=command.description,
            city=command.city,
            street=command.street,
            building_number=command.building_number,
            block=command.block,
            auditorium=command.auditorium,
        )

        event = await self._event_repo.update(event)

        await self._transactional_manager.commit()

        return event