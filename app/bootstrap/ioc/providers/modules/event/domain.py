from dishka import Provider, Scope, provide

from modules.event.domain.repository.event_registration import IEventRegistrationRepository
from modules.event.domain.rules.event_registration import UserRegisteredEventRule
from modules.event.domain.services.event_registration import EventRegistrationService


class ServiceDomainEventProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def event_registration(
        self,
        event_registration_repo: IEventRegistrationRepository,
        is_user_registered_event_rule: UserRegisteredEventRule,
    ) -> EventRegistrationService:
        return EventRegistrationService(
            _event_registration_repo=event_registration_repo,
            _is_user_registered_event_rule=is_user_registered_event_rule,
        )


class RuleDomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_registered_event(
        self,
        event_registration_repo: IEventRegistrationRepository,
    ) -> UserRegisteredEventRule:
        return UserRegisteredEventRule(
            _event_registration_repo=event_registration_repo,
        )