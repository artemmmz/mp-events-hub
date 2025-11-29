from dataclasses import dataclass

from seedwork.domain.value_objects.common.exceptions import ValueException


@dataclass(eq=False)
class InvalidBuildingBlockException(ValueException):
    value: str

    @property
    def message(self) -> str:
        return f"Неверный формат корпуса: '{self.value}'. Допустимо: '2', '5а', '12A', '3Б'."


@dataclass(eq=False)
class InvalidAuditoriumException(ValueException):
    value: str

    @property
    def message(self) -> str:
        return f"Неверный формат аудитории: '{self.value}'. Допустимо: '2', '5а', '12A', '3Б'."


@dataclass(eq=False)
class EventInPastException(ValueException):
    value: str

    @property
    def message(self) -> str:
        return f"Невозможно создать событие в прошлом: '{self.value}'"