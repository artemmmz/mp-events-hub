from dishka import Provider, Scope, provide

from modules.auth.domain.repository.user import (
    IUserRepository,
)
from modules.auth.domain.rules.user import (
    UniqueEmailRule,
    UniqueUserRule,
)


class RulesAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def unique_email(
        self,
        user_repository: IUserRepository,
    ) -> UniqueEmailRule:
        return UniqueEmailRule(
            _user_repository=user_repository,
        )

    @provide
    def unique_user(
        self,
        user_repository: IUserRepository,
    ) -> UniqueUserRule:
        return UniqueUserRule(
            _user_repository=user_repository,
        )