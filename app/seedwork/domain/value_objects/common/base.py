from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from seedwork.domain.value_objects.common.exceptions import EmptyValueException


@dataclass(
    frozen=True,
    slots=True,
)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...


ValueType = TypeVar("ValueType", bound=Any)


@dataclass(
    frozen=True,
    slots=True,
)
class BaseSimpleValueObject(
    BaseValueObject,
    Generic[ValueType],
    ABC,
):
    _value: ValueType

    def validate(self) -> None:
        if self._value is None:
            raise EmptyValueException()

    @property
    def value(self) -> ValueType:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseSimpleValueObject):
            raise NotImplementedError

        return self._value == other._value


@dataclass(
    frozen=True,
    slots=True,
)
class BaseCompositeValueObject(
    BaseValueObject,
    ABC,
):
    ...