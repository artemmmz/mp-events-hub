from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from bootstrap.settings import Settings


class RedisProvider(Provider):
    def __init__(
        self,
        redis_client: Redis | None = None,
    ) -> None:
        super().__init__()
        self.redis_client: Redis | None = redis_client

    @provide(scope=Scope.APP)
    def redis(
        self,
        settings: Settings,
    ) -> Redis:
        if self.redis_client:
            return self.redis_client

        else:
            return Redis(
                host=settings.redis.host,
                port=settings.redis.port,
                db=settings.redis.db,
                password=settings.redis.password,
            )