from enum import Enum


class RoleValue(
    Enum,
):
    USER = "user"
    ADMIN = "admin"

    def validate(self) -> None:
        pass