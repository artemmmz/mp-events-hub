from dishka import Provider, Scope, provide

from faststream.rabbit import RabbitBroker

from bootstrap.event_map import event_queue_map
from seedwork.infra.event_bus.base import IEventBus
from seedwork.infra.event_bus.fs import FsEventBus

class EventBusProvider(Provider):
    @provide(scope=Scope.APP)
    def faststream_rmq(
        self,
        broker: RabbitBroker,
    ) -> IEventBus:
        return FsEventBus(
            _broker=broker,
            _event_queue_map=event_queue_map,
        )
