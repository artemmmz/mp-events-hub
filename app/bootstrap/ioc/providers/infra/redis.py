from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from bootstrap.settings import Settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def redis(
        self,
        settings: Settings,
    ) -> Redis:
        return Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            password=settings.redis.password,
        )