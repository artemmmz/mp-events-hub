from abc import ABC, abstractmethod

from infra.pg.models import RoleOrm
from modules.auth.domain.value_object.roles import RoleValue
from seedwork.infra.dm.base import BaseDataMapper


class IRoleDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_name(self, role: RoleValue) -> RoleOrm | None:
        ...