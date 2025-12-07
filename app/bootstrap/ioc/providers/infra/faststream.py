from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from bootstrap.settings import Settings


class FastStreamProvider(Provider):
    def __init__(
        self,
        connection_string: str | None = None,
    ) -> None:
        super().__init__()
        self.connection_string: str | None = connection_string

    @provide(scope=Scope.APP)
    async def faststream(self, broker: RabbitBroker) -> FastStream:
        app = FastStream(broker)
        return app

    @provide(scope=Scope.APP)
    async def broker(
        self,
        settings: Settings,
    ) -> AsyncIterable[RabbitBroker]:
        connection_string: str = settings.rmq.rabbit_broker_url

        if self.connection_string:
            connection_string = self.connection_string

        async with RabbitBroker(
            url=connection_string,
        ) as broker:
            yield broker