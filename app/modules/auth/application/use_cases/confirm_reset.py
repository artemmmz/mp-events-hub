from dataclasses import dataclass

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from modules.auth.application.services.jwt import JwtService
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.exceptions import UserNotFoundException
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
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
    _jwt_service: JwtService
    _user_repo: IUserRepository
    _user_dm: IUserKvDm
    _transactional_manager: ITransactionManager

    async def act(
        self,
        command: ConfirmResetPasswordCommand,
    ) -> JwtTokenValue:
        user: User | None = await self._user_repo.find_by_email(
            email=EmailValue(command.email),
        )

        if not user:
            raise UserNotFoundException(email=command.email)

        confirm_code: str | None = await self._user_dm.get_confirm_code_by_email(
            email=EmailValue(command.email),
        )
        new_password: str | None = await self._user_dm.get_password_by_email(
            email=EmailValue(command.email),
        )

        user.reset_password(
            new_password=new_password,
            input_code=ConfirmCodeValue(command.confirm_code),
            stored_code=ConfirmCodeValue(confirm_code),
        )

        await self._user_repo.update(user)
        await self._transactional_manager.commit()

        token: JwtTokenValue = self._jwt_service.issue_token(
            payload={"user_id": str(user.id.value)},
        )

        return token