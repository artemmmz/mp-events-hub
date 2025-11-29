from seedwork.domain.event import DomainEvent
from seedwork.infra.event_bus.base import QueueRmq

from modules.auth.domain.events import RegistrationRequestedUserEvent
from modules.email.infra.rmq.queues import REGISTRATION_REQUESTED_USER_EVENT_QUEUE

event_queue_map: dict[type[DomainEvent], QueueRmq] = {
    RegistrationRequestedUserEvent: REGISTRATION_REQUESTED_USER_EVENT_QUEUE,
}