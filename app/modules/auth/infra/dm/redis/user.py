from asyncpg.pgproto.pgproto import timedelta

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.infra.dm.base import BaseRedisDataMapper


class UserRedisDm(
    IUserKvDm,
    BaseRedisDataMapper,
):
    async def save_confirm_code(
        self,
        user_id: EntityIdValue,
        confirm_code: ConfirmCodeValue,
        ttl: timedelta,
    ) -> None:
        await self._redis.set(
            name=f"user:confirm:{user_id.value}",
            value=confirm_code.value,
            ex=ttl,
        )

    async def get_confirm_code(
        self,
        user_id: EntityIdValue,
    ) -> str | None:
        code = await self._redis.get(f"user:confirm:{user_id.value}")

        if code is None:
            return None

        return code.decode()