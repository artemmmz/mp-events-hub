from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from seedwork.domain.exception import DomainException
from seedwork.domain.types import Number


@dataclass(eq=False)
class ValueException(
    DomainException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        message = "Value object exception!"

        return message


@dataclass(eq=False)
class EmptyValueException(ValueException):
    @property
    def message(self) -> str:
        message = "Value cannot be empty!"

        return message


@dataclass(eq=False)
class ValueTooLongException(ValueException):
    _max_len: int
    current_len: int

    @property
    def message(self) -> str:
        message = f"Value too long! Current len {self.current_len}, max len {self._max_len}"

        return message


@dataclass(eq=False)
class ValueTooShortException(ValueException):
    _min_len: int
    current_len: int

    @property
    def message(self) -> str:
        message = f"Value too short! Current len {self.current_len}, min len {self._min_len}"

        return message


@dataclass(eq=False)
class InvalidNumberTypeException(ValueException):
    @property
    def message(self) -> str:
        return "Value must be a number (int, float, Decimal)!"


@dataclass(eq=False)
class NotPositiveNumberException(ValueException):
    value: Number

    @property
    def message(self) -> str:
        return f"Value must be positive! Got {self.value}"