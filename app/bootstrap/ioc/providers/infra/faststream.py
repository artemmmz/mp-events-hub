from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from bootstrap.settings import Settings


class FastStreamProvider(Provider):
    @provide(scope=Scope.APP)
    async def faststream(self, broker: RabbitBroker) -> FastStream:
        app = FastStream(broker)
        return app

    @provide(scope=Scope.APP)
    async def broker(self, settings: Settings) -> AsyncIterable[RabbitBroker]:
        async with RabbitBroker(
            url=settings.rmq.rabbit_broker_url,
        ) as broker:
            yield broker

