from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import and_, select, delete

from modules.event.infra.pg.models import EventRegistrationOrm
from seedwork.infra.dm.base import BaseDataMapper, BaseAlchemyDataMapper
from seedwork.infra.pg.excpetions import MissingRequiredFieldException


class IEventRegistrationDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_id(
        self,
        user_id: UUID,
        event_id: UUID,
    ) -> EventRegistrationOrm:
        ...

    @abstractmethod
    async def delete(self, _id: UUID) -> None:
        ...


class EventRegistrationAlchemyDm(
    IEventRegistrationDm,
    BaseAlchemyDataMapper,
):
    async def get_by_id(
        self,
        user_id: UUID,
        event_id: UUID,
    ) -> EventRegistrationOrm:
        result = await self._session.execute(
            select(EventRegistrationOrm)
            .where(
                and_(
                    EventRegistrationOrm.event_uid == event_id,
                    EventRegistrationOrm.user_uid == user_id,
                )
            )
        )

        event_registration_orm: EventRegistrationOrm | None = (
            result.scalar_one_or_none()
        )

        if event_registration_orm:
            return event_registration_orm

        raise MissingRequiredFieldException(
            required_field="",
        )

    async def delete(self, _id: UUID) -> None:
        await self._session.execute(
            delete(EventRegistrationOrm)
            .where(EventRegistrationOrm.uid == _id)
        )