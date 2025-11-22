from dataclasses import dataclass

from modules.auth.domain.entities.user import User
from infra.pg.models.user import UserOrm
from modules.auth.domain.value_object.roles import RoleValue
from seedwork.application.mapper import BaseMapper


@dataclass
class UserMapper(BaseMapper):
    @staticmethod
    def to_orm(user: User) -> UserOrm:
        return UserOrm(
            uid=user.id,
            name=user.name.value,
            second_name=user.second_name.value,
            group_number=user.group_number.value,
            email=user.email.value,
            hash_password=user.hash_password,
        )

    @staticmethod
    def to_entity(user_orm: UserOrm) -> User:
        return User.create(
            name=user_orm.name,
            second_name=user_orm.second_name,
            group_number=user_orm.group_number,
            email=user_orm.email,
            password=user_orm.hash_password,
            role=RoleValue(user_orm.role.name)
        )
