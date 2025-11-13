from enum import Enum

from seedwork.domain.value_objects.common.base import BaseValueObject


class RoleValue(
    BaseValueObject,
    Enum,
):
    USER = "user"
    ADMIN = "admin"

    def validate(self) -> None:
        pass