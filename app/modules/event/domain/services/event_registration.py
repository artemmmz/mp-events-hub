from dataclasses import dataclass

from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.event_registration import EventRegistration
from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.rules.exceptions import UserAlreadyRegisteredException
from modules.event.domain.aggregate.user import User
from modules.event.domain.rules.event_registration import UserRegisteredEventRule


@dataclass
class EventRegistrationService:
    _event_registration_repo: IEventRegistrationRepository
    _is_user_registered_event_rule: UserRegisteredEventRule

    async def register_user_for_event(
        self,
        user: User,
        event: Event,
    ) -> EventRegistration:
        if await self._is_user_registered_event_rule.is_broken(
                user_id=user.id,
                event_id=event.id,
        ):
            raise UserAlreadyRegisteredException(
                user_id=user.id,
                event_id=event.id,
            )

        registration = EventRegistration.create(
            user_id=user.id.value,
            event_id=event.id.value,
        )

        await self._event_registration_repo.create(registration)

        return registration