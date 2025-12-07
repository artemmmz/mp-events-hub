from abc import ABC, abstractmethod

from seedwork.infra.pg.models import RoleOrm
from seedwork.domain.value_objects.role import RoleValue
from seedwork.infra.dm.base import BaseDataMapper


class IRoleDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_name(self, role: RoleValue) -> RoleOrm | None:
        ...

    @abstractmethod
    async def create(self, role_orm: RoleOrm) -> None:
        ...