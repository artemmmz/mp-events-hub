from abc import ABC, abstractmethod
from uuid import UUID

from modules.auth.infra.pg.models import UserAuthOrm
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
    ) -> UserAuthOrm | None:
        ...