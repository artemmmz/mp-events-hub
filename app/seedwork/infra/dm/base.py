from abc import ABC
from dataclasses import dataclass

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDataMapper(ABC):
    ...


@dataclass
class BaseAlchemyDataMapper(BaseDataMapper):
    _session: AsyncSession


@dataclass
class BaseRedisDataMapper(BaseDataMapper):
    _redis: Redis
