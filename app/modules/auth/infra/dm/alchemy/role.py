from sqlalchemy import select

from infra.pg.models import RoleOrm
from modules.auth.application.interface.dm.sql.roles import IRoleDm
from modules.auth.domain.value_object.roles import RoleValue
from seedwork.infra.dm.alchemy import BaseAlchemyDataMapper


class RoleAlchemyDm(
    IRoleDm,
    BaseAlchemyDataMapper,
):
    async def get_by_name(self, role: RoleValue) -> RoleOrm | None:
        result = await self._session.execute(
            select(RoleOrm)
            .where(RoleOrm.name == role.value)
        )

        role_orm: RoleOrm | None = result.scalar_one_or_none()

        return role_orm