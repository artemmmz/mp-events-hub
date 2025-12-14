from dataclasses import dataclass

from seedwork.domain.value_objects.common.base import ValueType
from seedwork.domain.value_objects.common.exceptions import ValueException


@dataclass
class GroupNumberFormatException(ValueException):
    group_number: ValueType

    @property
    def message(self) -> str:
        return f"Номер группы должен соответствовать формату 123-456, получено: {self.group_number}"


@dataclass
class EmailFormatException(ValueException):
    email: ValueType

    @property
    def message(self) -> str:
        return f"Неправильный формат почты: {self.email}"


@dataclass
class RoleValueException(ValueException):
    value: str

    @property
    def message(self) -> str:
        return f"Недопустимое значение роли: {self.value}"


@dataclass
class MediaTypeNotExistException(ValueException):
    media_type: str

    @property
    def message(self) -> str:
        return f"Media type: {self.media_type} does not exist"