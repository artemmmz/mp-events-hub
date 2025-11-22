from abc import ABC, abstractmethod

from modules.auth.domain.entities.user import User
from seedwork.domain.value_objects.user import NameValue, GroupNumberValue, EmailValue
from seedwork.domain.repository import BaseRepository


class IUserRepository(
    BaseRepository,
    ABC,
):
    @abstractmethod
    async def create(self, user: User) -> None:
        ...

    @abstractmethod
    async def is_email_taken(self, email: EmailValue) -> bool:
        ...

    @abstractmethod
    async def is_user_duplicate(
        self,
        name: NameValue,
        second_name: NameValue,
        group_number: GroupNumberValue,
    ) -> bool:
        ...

    @abstractmethod
    async def get_by_email(
        self,
        email: EmailValue,
    ) -> User | None:
        ...