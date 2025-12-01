from seedwork.domain.events.base import DomainEvent
from seedwork.infra.event_bus.base import QueueRmq

from seedwork.domain.events.auth import (
    RequestedRegistrationUserEvent,
    ConfirmRegistrationUserEvent,
)
from seedwork.infra.rmq.queues import (
    REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
    CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
)

event_queue_map: dict[type[DomainEvent], QueueRmq] = {
    RequestedRegistrationUserEvent: REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
    ConfirmRegistrationUserEvent: CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
}