from dishka import Provider, Scope, provide

from bootstrap.settings import Settings


class SettingProvider(Provider):
    @provide(scope=Scope.APP)
    def setting(self) -> Settings:
        return Settings()