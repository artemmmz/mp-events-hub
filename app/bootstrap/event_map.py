from seedwork.domain.event import DomainEvent
from seedwork.infra.event_bus.base import QueueRmq

event_queue_map: dict[type[DomainEvent], QueueRmq] = {

}