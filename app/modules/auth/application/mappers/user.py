from dataclasses import dataclass

from auth.application.mappers.role import RoleMapper
from auth.domain.entities.user import User
from infra.pg.models.role import RoleOrm
from infra.pg.models.user import UserOrm
from seedwork.application.mapper import BaseMapper


@dataclass
class UserMapper(BaseMapper):
    _role_mapper: RoleMapper

    def to_orm(self, user: User) -> UserOrm:
        role: RoleOrm = self._role_mapper.to_orm(role=user.role)

        return UserOrm(
            uid=user.id.value,
            name=user.name.value,
            second_name=user.second_name.value,
            group_number=user.group_number.value,
            email=user.email.value,
            hash_password=user.hash_password,
            role=role,
        )
