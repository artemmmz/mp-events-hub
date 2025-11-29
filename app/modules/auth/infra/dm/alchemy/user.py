from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infra.pg.models import UserOrm
from modules.auth.application.interface.dm.sql.user import IUserDm
from seedwork.infra.dm.alchemy import BaseAlchemyDataMapper


class UserAlchemyDm(
    IUserDm,
    BaseAlchemyDataMapper,
):
    async def get_by_uid(
        self,
        uid: UUID,
        role_load: bool = True,
    ) -> UserOrm | None:
        query = select(UserOrm).where(UserOrm.uid == uid)

        if role_load:
            query = query.options(joinedload(UserOrm.role))

        result = await self._session.execute(query)

        user_orm: UserOrm | None = result.scalar_one_or_none()

        return user_orm