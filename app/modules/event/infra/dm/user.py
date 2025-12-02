from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from modules.event.infra.pg.models import UserEventOrm
from seedwork.infra.dm.base import BaseAlchemyDataMapper, BaseDataMapper
from seedwork.infra.pg.excpetions import MissingRequiredFieldException


class IUserDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_id(
        self,
        _id: UUID,
        events_created_load: bool,
        registered_events_load: bool,
    ) -> UserEventOrm:
        ...


class UserAlchemyDm(
    IUserDm,
    BaseAlchemyDataMapper,
):
    async def get_by_id(
        self,
        _id: UUID,
        events_created_load: bool,
        registered_events_load: bool,
    ) -> UserEventOrm:
        query = select(UserEventOrm).where(UserEventOrm.uid == _id)

        if events_created_load:
            query = query.options(
                selectinload(UserEventOrm.events_created)
            )

        if registered_events_load:
            query = query.options(
                selectinload(UserEventOrm.registered_events)
            )

        result = await self._session.execute(query)

        user_orm: UserEventOrm | None = result.scalar_one_or_none()

        if user_orm:
            return user_orm

        raise MissingRequiredFieldException(
            required_field="user_event.uid",
        )