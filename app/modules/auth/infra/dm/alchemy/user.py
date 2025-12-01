from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from modules.auth.infra.pg.models import UserAuthOrm
from modules.auth.application.interface.dm.sql.user import IUserDm
from seedwork.infra.dm.base import BaseAlchemyDataMapper


class UserAlchemyDm(
    IUserDm,
    BaseAlchemyDataMapper,
):
    async def get_by_uid(
        self,
        uid: UUID,
        role_load: bool = True,
    ) -> UserAuthOrm | None:
        query = select(UserAuthOrm).where(UserAuthOrm.uid == uid)

        if role_load:
            query = query.options(joinedload(UserAuthOrm.role))

        result = await self._session.execute(query)

        user_orm: UserAuthOrm | None = result.scalar_one_or_none()

        return user_orm