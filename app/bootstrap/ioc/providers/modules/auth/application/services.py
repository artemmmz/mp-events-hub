from dishka import Provider, Scope, provide

from bootstrap.settings import Settings
from modules.auth.application.services.jwt import JwtService


class ServiceAuthProvider(Provider):
    @provide(scope=Scope.APP)
    def jwt(self, settings: Settings) -> JwtService:
        return JwtService(
            _secret_key=settings.auth.secret_key,
            _access_token_lifetime=settings.auth.access_token_lifetime,
            _algorithm=settings.auth.algorithm,
        )