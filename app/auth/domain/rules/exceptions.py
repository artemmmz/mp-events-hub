from dataclasses import dataclass

from seedwork.domain.rules import BusinessRuleException
from seedwork.domain.value_objects.user import EmailValue, NameValue, GroupNumberValue


@dataclass
class EmailAlreadyExistsException(BusinessRuleException):
    email: EmailValue

    @property
    def message(self) -> str:
        return f"User with email '{self.email.value}' already exists."


@dataclass
class UserAlreadyExistsException(BusinessRuleException):
    name: NameValue
    second_name: NameValue
    group_number: GroupNumberValue

    @property
    def message(self) -> str:
        return (
            f"User '{self.name.value} {self.second_name.value}' "
            f"from group '{self.group_number.value}' already exists."
        )