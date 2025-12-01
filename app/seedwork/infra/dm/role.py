from sqlalchemy import select

from seedwork.infra.pg.models import RoleOrm
from seedwork.application.interface.dm.sql.roles import IRoleDm
from seedwork.domain.value_objects.role import RoleValue
from seedwork.infra.dm.base import BaseAlchemyDataMapper


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