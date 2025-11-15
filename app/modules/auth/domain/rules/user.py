from dataclasses import dataclass, field

from auth.domain.repository.user import IUserRepository
from seedwork.domain.rules import BusinessRule
from seedwork.domain.value_objects.user import EmailValue, NameValue, GroupNumberValue


@dataclass
class UniqueEmailRule(BusinessRule):
    _user_repository: IUserRepository

    __message: str = field(default="Email is already taken", init=False)

    async def is_broken(self, email: EmailValue) -> bool:
        return await self._user_repository.is_email_taken(email=email)


@dataclass
class UniqueUserRule(BusinessRule):
    _user_repository: IUserRepository

    __message: str = field(default="User with this data already exists", init=False)

    async def is_broken(
        self,
        name: NameValue,
        second_name: NameValue,
        group_number: GroupNumberValue,
    ) -> bool:
        return await self._user_repository.is_user_duplicate(
            name=name,
            second_name=second_name,
            group_number=group_number,
        )