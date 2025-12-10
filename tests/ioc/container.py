import os
import sys

from dishka import AsyncContainer, make_async_container
from redis.asyncio import Redis

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.bootstrap.ioc.container import DEV_PROVIDERS
from app.bootstrap.ioc.providers.infra import (
    AlchemyProvider,
    FastStreamProvider,
    RedisProvider,
)


def get_test_container(
    connection_string: str,
    local_rmq_url: str,
    redis: Redis
) -> AsyncContainer:
    container: AsyncContainer = make_async_container(
        *DEV_PROVIDERS,
        AlchemyProvider(connection_string=connection_string),
        FastStreamProvider(connection_string=local_rmq_url),
        RedisProvider(redis_client=redis),
    )

    return container