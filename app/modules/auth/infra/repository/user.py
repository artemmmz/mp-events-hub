from dataclasses import dataclass

from sqlalchemy import select, exists, and_
from sqlalchemy.orm import joinedload

from infra.pg.models import RoleOrm
from modules.auth.application.interface.dm import IRoleDm
from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.entities.user import User
from modules.auth.domain.repository.user import IUserRepository
from infra.pg.models.user import UserOrm
from seedwork.domain.value_objects.user import EmailValue, NameValue, GroupNumberValue
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class UserAlchemyRepository(
    IUserRepository,
    BaseAlchemyRepository,
):
    _mapper: UserMapper
    _role_dm: IRoleDm

    async def create(self, user: User) -> None:
        role_orm: RoleOrm = await (
            self._role_dm.get_by_name(role=user.role)
        )

        user_orm: UserOrm = self._mapper.to_orm(user=user)
        user_orm.role = role_orm

        self._session.add(user_orm)

    async def is_email_taken(self, email: EmailValue) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(UserOrm.email == email.value)
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

    async def get_by_email(
        self,
        email: EmailValue,
    ) -> User | None:
        result = await self._session.execute(
            select(UserOrm)
            .where(UserOrm.email == email.value)
            .options(
                joinedload(UserOrm.role)
            )
        )

        user_orm: UserOrm | None = result.scalar_one_or_none()

        if user_orm:
            user: User = self._mapper.to_entity(user_orm)
            return user

        else:
            return None
