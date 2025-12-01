from abc import ABC, abstractmethod
from dataclasses import dataclass

from seedwork.domain.exception import DomainException


class AccessControlException(
    DomainException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Domain Service Exception"


@dataclass
class ExactRoleMismatchException(AccessControlException):
    user_role: str
    required_role: str

    @property
    def message(self) -> str:
        return f"User role '{self.user_role}' must be exactly '{self.required_role}'"


@dataclass
class MinRoleTooLowException(AccessControlException):
    user_role: str
    minimum_role: str

    @property
    def message(self) -> str:
        return f"User role '{self.user_role}' must be at least '{self.minimum_role}'"
