from abc import ABC, abstractmethod
from uuid import UUID

from infra.pg.models import UserOrm
from seedwork.infra.dm.base import BaseDataMapper


class IUserDm(
    BaseDataMapper,
    ABC,
):
    @abstractmethod
    async def get_by_uid(
        self,
        uid: UUID,
        role_load: bool = True,
    ) -> UserOrm | None:
        ...