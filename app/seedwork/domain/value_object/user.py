from enum import Enum


class RoleValue(
    Enum,
):
    USER = "user"
    ORGANIZER = "organizer"
    ADMIN = "admin"

    def validate(self) -> None:
        pass
