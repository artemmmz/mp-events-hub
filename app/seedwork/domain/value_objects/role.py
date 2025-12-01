from enum import Enum


class RoleValue(
    Enum,
):
    USER = "user"
    ORGANIZER = "organizer"
    ADMIN = "admin"

    def validate(self) -> None:
        pass

    @property
    def level(self) -> int:
        return {
            RoleValue.USER: 1,
            RoleValue.ORGANIZER: 2,
            RoleValue.ADMIN: 3,
        }[self]
