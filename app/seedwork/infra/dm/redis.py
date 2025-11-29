from dataclasses import dataclass

from redis.asyncio import Redis

from seedwork.infra.dm.base import BaseDataMapper


@dataclass
class BaseRedisDataMapper(BaseDataMapper):
    _redis: Redis
