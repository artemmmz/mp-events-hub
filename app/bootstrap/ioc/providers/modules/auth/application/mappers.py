from dishka import Provider, Scope, provide

from modules.auth.application.mappers.role import RoleMapper
from modules.auth.application.mappers.user import UserMapper


class MapperAuthProvider(Provider):
    scope = Scope.APP

    @provide
    def user(self, role_mapper: RoleMapper) -> UserMapper:
        return UserMapper(
            _role_mapper=role_mapper,
        )

    @provide
    def role(self) -> RoleMapper:
        return RoleMapper()