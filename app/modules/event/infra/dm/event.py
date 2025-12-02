from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from modules.event.infra.pg.models import EventOrm, AddressOrm
from seedwork.infra.dm.base import BaseDataMapper, BaseAlchemyDataMapper
from seedwork.infra.pg.excpetions import MissingRequiredFieldException


class IEventDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_id(
        self,
        _id: UUID,
    ) -> EventOrm:
        ...


class EventAlchemyDm(
    IEventDm,
    BaseAlchemyDataMapper,
):
    async def get_by_id(
        self,
        _id: UUID,
    ) -> EventOrm:
        query = (
            select(EventOrm)
            .where(EventOrm.uid == _id)
            .options(
                joinedload(EventOrm.address)
                .joinedload(AddressOrm.building)
            )
        )

        result = await self._session.execute(query)

        event_orm: EventOrm | None = result.scalar_one_or_none()

        if event_orm:
            return event_orm

        raise MissingRequiredFieldException(
            required_field="event.uid",
        )