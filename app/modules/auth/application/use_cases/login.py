from dataclasses import dataclass

from modules.auth.application.services.jwt import JwtService
from modules.auth.domain.entities.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.exceptions import (
    UserNotFoundException,
    InvalidPasswordException,
)
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.jwt import JwtTokenValue
from seedwork.domain.value_objects.user import EmailValue


@dataclass
class LoginCommand:
    email: str
    password: str


@dataclass
class LoginUseCase(
    BaseUseCase[LoginCommand, JwtTokenValue]
):
    _user_repo: IUserRepository
    _jwt_service: JwtService

    async def act(self, command: LoginCommand) -> JwtTokenValue:
        user: User | None = await self._user_repo.get_by_email(
            email=EmailValue(_value=command.email)
        )

        if not user:
            raise UserNotFoundException(email=command.email)

        is_valid: bool = user.check_password(password=command.password)

        if not is_valid:
            raise InvalidPasswordException(email=command.email)

        token: JwtTokenValue = self._jwt_service.issue_token(
            payload={"user_id": str(user.id)},
        )

        return token
