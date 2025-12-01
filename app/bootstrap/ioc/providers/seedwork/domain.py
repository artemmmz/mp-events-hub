from dishka import Provider, Scope, provide

from seedwork.domain.services.authorization import AuthorizationService


class ServiceDomainProvider(Provider):
    @provide(scope=Scope.APP)
    def authorization(self) -> AuthorizationService:
        return AuthorizationService()