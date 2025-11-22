from dataclasses import dataclass

from modules.auth.domain.entities.user import User
from infra.pg.models.user import UserOrm
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
