from dataclasses import dataclass

from sqlalchemy import select, update, exists, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.inspection import inspect

from infra.pg.excpetions import MissingRequiredFieldException
from infra.pg.models import RoleOrm
from modules.auth.application.interface.dm.sql.roles import IRoleDm
from modules.auth.application.interface.dm.sql.user import IUserDm
from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.aggregate.user import User
from modules.auth.domain.repository.user import IUserRepository
from infra.pg.models.user import UserOrm
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.domain.value_objects.user import (
    EmailValue,
    NameValue,
    GroupNumberValue,
)
from seedwork.infra.repository.alchemy import BaseAlchemyRepository


@dataclass
class UserAlchemyRepository(
    IUserRepository,
    BaseAlchemyRepository,
):
    _mapper: UserMapper
    _role_dm: IRoleDm
    _user_dm: IUserDm

    async def create(self, user: User) -> None:
        print(f"user_entity_uid: {user.id.value}")
        role_orm: RoleOrm = await (
            self._role_dm.get_by_name(role=user.role)
        )

        user_orm: UserOrm = self._mapper.to_orm(user=user)
        user_orm.role_uid = role_orm.uid

        self._session.add(user_orm)

    async def update(self, user: User) -> User:
        user_orm: UserOrm | None = await (
            self._user_dm.get_by_uid(uid=user.id.value, role_load=False)
        )

        if user_orm is None:
            raise MissingRequiredFieldException(
                required_field=user.id.value,
            )

        new_data: UserOrm = self._mapper.to_orm(user)

        self._copy_orm_fields(source=new_data, target=user_orm)

        role_orm = await self._role_dm.get_by_name(role=user.role)

        user_orm.role_uid = role_orm.uid

        new_user: User = self._mapper.to_entity(user_orm=user_orm)

        return new_user

    async def is_email_taken(self, email: EmailValue) -> bool:
        result = await self._session.execute(
            select(
                exists()
                .where(
                    and_(
                        UserOrm.email == email.value,
                        UserOrm.email_confirm.is_(True),
                    )
                )
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
                        UserOrm.email_confirm.is_(True),
                    )
                )
            )
        )
        return result.scalar()

    async def get_by_id(
        self,
        required_id: EntityIdValue,
    ) -> User | None:
        result = await self._session.execute(
            select(UserOrm)
            .where(UserOrm.uid == required_id.value)
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

    async def get_by_email(
        self,
        email: EmailValue,
    ) -> User | None:
        result = await self._session.execute(
            select(UserOrm)
            .where(
                and_(
                    UserOrm.email == email.value,
                    UserOrm.email_confirm.is_(True),
                )
            )
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

    async def confirm_user(
        self,
        email: EmailValue,
    ) -> None:
        await self._session.execute(
            update(UserOrm)
            .where(UserOrm.email == email.value)
            .values(email_confirm=True)
        )

    @staticmethod
    def _copy_orm_fields(source: UserOrm, target: UserOrm) -> None:
        mapper = inspect(UserOrm)

        attrs = list(mapper.column_attrs.values())

        for attr in attrs:
            name: str = attr.key

            if name in ("id", "uid", "role", "role_id", "created_at"):
                continue

            setattr(target, name, getattr(source, name))
