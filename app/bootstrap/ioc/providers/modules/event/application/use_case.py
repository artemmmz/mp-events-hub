from dishka import Provider, Scope, provide

from modules.event.application.use_cases.event.create import (
    CreateEventUseCase,
)
from modules.event.application.use_cases.auth.confirm import (
    ConfirmRegisterUseCase,
)
from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.user import IUserRepository
from seedwork.domain.services.authorization import AuthorizationService
from seedwork.infra.transaction_manager.base import ITransactionManager


class UseCaseEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def create_event(
        self,
        authorization_service: AuthorizationService,
        user_repo: IUserRepository,
        event_repo: IEventRepository,
        transactional_manager: ITransactionManager,
    ) -> CreateEventUseCase:
        return CreateEventUseCase(
            _authorization_service=authorization_service,
            _user_repo=user_repo,
            _event_repo=event_repo,
            _transactional_manager=transactional_manager,
        )

    @provide
    def confirm_register(
        self,
        user_repo: IUserRepository,
        transaction_manager: ITransactionManager,
    ) -> ConfirmRegisterUseCase:
        return ConfirmRegisterUseCase(
            _user_repo=user_repo,
            _transaction_manager=transaction_manager,
        )