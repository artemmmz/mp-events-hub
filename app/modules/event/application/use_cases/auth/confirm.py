from dataclasses import dataclass
from uuid import UUID

from modules.event.domain.aggregate.user import User
from modules.event.domain.repository.user import IUserRepository
from seedwork.application.use_case import BaseUseCase
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class ConfirmRegisterCommand:
    user_id: UUID
    role: str


@dataclass
class ConfirmRegisterUseCase(
    BaseUseCase[ConfirmRegisterCommand, None],
):
    _user_repo: IUserRepository
    _transaction_manager: ITransactionManager

    async def act(self, command: ConfirmRegisterCommand) -> None:
        user: User = User.create(
            _id=command.user_id,
            role=command.role,
        )

        await self._user_repo.create(user)

        await self._transaction_manager.commit()
