from dishka import Provider, Scope, provide

from modules.event.application.validators.event import EventImageValidator


class ValidatorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def image_validator(self) -> EventImageValidator:
        return EventImageValidator()