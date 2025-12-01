from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.services.exceptions import (
    ExactRoleMismatchException,
    MinRoleTooLowException,
)


class AuthorizationService:
    @staticmethod
    def check_exact_role(
        user_role: RoleValue,
        required_role: RoleValue,
    ) -> None:
        if user_role != required_role:
            raise ExactRoleMismatchException(
                user_role=user_role.name,
                required_role=required_role.name,
            )

    @staticmethod
    def check_min_role(
        user_role: RoleValue,
        minimum_role: RoleValue,
    ) -> None:
        if user_role.level < minimum_role.level:
            raise MinRoleTooLowException(
                user_role=user_role.name,
                minimum_role=minimum_role.name,
            )