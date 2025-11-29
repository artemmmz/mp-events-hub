from dataclasses import dataclass

from modules.auth.domain.aggregate.user import User
from infra.pg.models.user import UserOrm
from modules.auth.domain.value_object.roles import RoleValue
from seedwork.application.mapper import BaseMapper
from seedwork.domain.value_objects.common.entity import EntityIdValue
from seedwork.domain.value_objects.user import NameValue, GroupNumberValue, EmailValue


@dataclass
class UserMapper(BaseMapper):
    @staticmethod
    def to_orm(user: User) -> UserOrm:
        return UserOrm(
            uid=user.id.value,
            name=user.name.value,
            second_name=user.second_name.value,
            group_number=user.group_number.value,
            email=user.email.value,
            hash_password=user.hash_password,
            email_confirm=user.email_confirm,
        )

    @staticmethod
    def to_entity(user_orm: UserOrm) -> User:
        return User(
            id=EntityIdValue(_value=user_orm.uid),
            _created_at=user_orm.created_at,
            _updated_at=user_orm.updated_at,
            name=NameValue(_value=user_orm.name),
            second_name=NameValue(_value=user_orm.second_name),
            group_number=GroupNumberValue(_value=user_orm.group_number),
            email=EmailValue(_value=user_orm.email),
            hash_password=user_orm.hash_password,
            role=RoleValue(user_orm.role.name),
            email_confirm=user_orm.email_confirm,
        )
