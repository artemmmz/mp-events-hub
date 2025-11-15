from dataclasses import dataclass

from sqlalchemy import select, exists, and_

from auth.application.mappers.user import UserMapper
from auth.domain.entities.user import User
from auth.domain.repository.user import IUserRepository
from infra.pg.models.user import UserOrm
from seedwork.domain.value_objects.user import EmailValue, NameValue, GroupNumberValue
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class UserAlchemyRepository(
    IUserRepository,
    BaseAlchemyRepository,
):
    _mapper: UserMapper

    async def create(self, entity: User) -> None:
        user_orm: UserOrm = self._mapper.to_orm(user=entity)

        self._session.add(user_orm)

    async def is_email_taken(self, email: EmailValue) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(UserOrm.email == email)
            )
        )
        return result.scalar()

    async def is_user_duplicate(
        self,
        name: NameValue,
        second_name: NameValue,
        group_number: GroupNumberValue,
    ) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(
                    and_(
                        UserOrm.name == name.value,
                        UserOrm.second_name == second_name.value,
                        UserOrm.group_number == group_number.value,
                    )
                )
            )
        )
        return result.scalar()
