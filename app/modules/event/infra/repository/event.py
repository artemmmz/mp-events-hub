from dataclasses import dataclass

from modules.event.infra.dm.event import IEventDm
from modules.event.infra.dm.user import IUserDm
from modules.event.infra.pg.models import UserEventOrm
from modules.event.infra.pg.models.event import EventOrm
from modules.event.domain.aggregate.event import Event
from modules.event.domain.repository.event import IEventRepository
from modules.event.infra.mappers.event import EventMapper
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class EventAlchemyRepository(
    IEventRepository,
    BaseAlchemyRepository,
):
    _mapper: EventMapper
    _event_dm: IEventDm
    _user_dm: IUserDm

    async def create(self, event: Event) -> None:
        event_orm: EventOrm = self._mapper.to_orm(event)
        user_orm: UserEventOrm = await self._user_dm.get_by_id(
            _id=event.created_by_user_id.value,
            events_created_load=False,
        )

        event_orm.created_by_user = user_orm

        self._session.add(event_orm)

    async def get_by_id(self, _id: EntityIdValue) -> Event:
        event_orm: EventOrm = await self._event_dm.get_by_id(_id=_id.value)

        event: Event = self._mapper.to_entity(event_orm=event_orm)

        return event