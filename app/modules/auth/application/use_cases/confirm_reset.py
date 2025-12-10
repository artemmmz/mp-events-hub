from dataclasses import dataclass

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.jwt import JwtTokenValue
from seedwork.domain.value_objects.user import EmailValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class ConfirmResetPasswordCommand:
    confirm_code: str
    email: str


@dataclass
class ConfirmResetPasswordUseCase(
    BaseUseCase[ConfirmResetPasswordCommand, JwtTokenValue],
):
    _user_repo: IUserRepository
    _user_dm: IUserKvDm
    _transactional_manager: ITransactionManager

    async def act(
        self,
        command: ConfirmResetPasswordCommand,
    ) -> JwtTokenValue:
        user: User = await self._user_repo.find_by_email(
            email=EmailValue(command.email),
        )

        user.reset_password