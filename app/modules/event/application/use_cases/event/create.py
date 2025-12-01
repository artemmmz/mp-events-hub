from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.user import IUserRepository
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.services.authorization import AuthorizationService
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.domain.value_objects.role import RoleValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class CreateEventCommand:
    user_id: UUID
    title: str
    scheduled_at: datetime
    description: str
    city: str
    street: str
    building_number: int
    block: str | None
    auditorium: str | None


@dataclass
class CreateEventUseCase(
    BaseUseCase[CreateEventCommand, Event],
):
    _authorization_service: AuthorizationService
    _user_repo: IUserRepository
    _event_repo: IEventRepository
    _transactional_manager: ITransactionManager

    async def act(self, command: CreateEventCommand) -> Event:
        user: User = await self._user_repo.get_by_id(
            required_id=EntityIdValue(_value=command.user_id),
        )

        self._authorization_service.check_min_role(
            user_role=user.role,
            minimum_role=RoleValue.ORGANIZER,
        )

        event: Event = user.create_event(
            title=command.title,
            scheduled_at=command.scheduled_at,
            description=command.description,
            city=command.city,
            street=command.street,
            building_number=command.building_number,
            block=command.block,
            auditorium=command.auditorium,
        )

        await self._event_repo.create(event=event)

        await self._transactional_manager.commit()

        return event