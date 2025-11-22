from dataclasses import dataclass

from modules.auth.application.services.jwt import JwtService
from modules.auth.domain.entities.user import User
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.domain.rules.user import UniqueEmailRule, UniqueUserRule
from modules.auth.domain.rules.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from modules.auth.domain.value_object.roles import RoleValue
from seedwork.application.use_case import BaseUseCase
from seedwork.domain.value_objects.jwt import JwtTokenValue
from seedwork.infra.transaction_manager.base import ITransactionManager


@dataclass
class RegisterCommand:
    name: str
    second_name: str
    group_number: str
    email: str
    password: str


@dataclass
class RegisterUseCase(
    BaseUseCase[RegisterCommand, JwtTokenValue],
):
    _transaction_manager: ITransactionManager
    _user_repository: IUserRepository
    _unique_email_rule: UniqueEmailRule
    _unique_user_rule: UniqueUserRule
    _jwt_manager: JwtService

    async def act(self, command: RegisterCommand) -> JwtTokenValue:
        user: User = User.create(
            name=command.name,
            second_name=command.second_name,
            group_number=command.group_number,
            email=command.email,
            password=command.password,
            role=RoleValue.USER,
        )

        if await self._unique_email_rule.is_broken(email=user.email):
            raise EmailAlreadyExistsException(email=user.email)

        if await self._unique_user_rule.is_broken(
            name=user.name,
            second_name=user.second_name,
            group_number=user.group_number,
        ):
            raise UserAlreadyExistsException(
                name=user.name,
                second_name=user.second_name,
                group_number=user.group_number,
            )

        await self._user_repository.create(user=user)

        token: JwtTokenValue = self._jwt_manager.issue_token(
            payload={"user_id": str(user.id)},
        )

        await self._transaction_manager.commit()

        return token

