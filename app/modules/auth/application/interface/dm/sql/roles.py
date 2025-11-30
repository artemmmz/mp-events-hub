from abc import ABC, abstractmethod

from infra.pg.models import RoleOrm
from seedwork.domain.value_object.user import RoleValue
from seedwork.infra.dm.base import BaseDataMapper


class IRoleDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_name(self, role: RoleValue) -> RoleOrm | None:
        ...