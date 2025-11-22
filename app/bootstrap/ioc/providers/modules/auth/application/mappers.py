from dishka import Provider, Scope, provide

from modules.auth.application.mappers.role import RoleMapper
from modules.auth.application.mappers.user import UserMapper


class MapperAuthProvider(Provider):
    scope = Scope.APP

    @provide
    def user(self) -> UserMapper:
        return UserMapper()

    @provide
    def role(self) -> RoleMapper:
        return RoleMapper()