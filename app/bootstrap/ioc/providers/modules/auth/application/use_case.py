from dishka import Provider, Scope, provide

from modules.auth.application.services.jwt import JwtService
from modules.auth.application.use_cases.login import LoginUseCase
from modules.auth.application.use_cases.register import RegisterUseCase
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.user import UniqueEmailRule, UniqueUserRule
from seedwork.infra.transaction_manager.base import ITransactionManager


class UseCaseAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register(
        self,
        transaction_manager: ITransactionManager,
        user_repository: IUserRepository,
        unique_email_rule: UniqueEmailRule,
        unique_user_rule: UniqueUserRule,
        jwt_manager: JwtService,
    ) -> RegisterUseCase:
        return RegisterUseCase(
            _transaction_manager=transaction_manager,
            _user_repository=user_repository,
            _unique_email_rule=unique_email_rule,
            _unique_user_rule=unique_user_rule,
            _jwt_manager=jwt_manager,
        )

    @provide
    def login(
        self,
        user_repo: IUserRepository,
        jwt_service: JwtService,
    ) -> LoginUseCase:
        return LoginUseCase(
            _user_repo=user_repo,
            _jwt_service=jwt_service,
        )