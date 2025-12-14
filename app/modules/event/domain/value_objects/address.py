from dataclasses import dataclass
from typing import Optional
import re

from modules.event.domain.value_objects.exceptions import (
    InvalidBuildingBlockException,
    InvalidAuditoriumException,
)
from seedwork.domain.value_objects.common.base import (
    BaseCompositeValueObject,
    BaseSimpleValueObject,
)
from seedwork.domain.value_objects.validators.lens import len_validate
from seedwork.domain.value_objects.validators.numbers import is_positive


@dataclass(frozen=True)
class AddressValue(BaseCompositeValueObject):
    city: "CityValue"
    street: "StreetValue"
    building: "BuildingValue"

    def validate(self) -> None:
        ...


class CityValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=30,
            min_len=2,
        )


class StreetValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=30,
            min_len=2,
        )


@dataclass(frozen=True)
class BuildingValue(BaseCompositeValueObject):
    number: "BuildingNumberValue"
    block: Optional["BuildingBlockValue"]
    auditorium: Optional["AuditoriumValue"]

    def validate(self) -> None:
        pass


class BuildingNumberValue(BaseSimpleValueObject[int, int]):
    def validate(self) -> None:
        is_positive(value=self._value)


class BuildingBlockValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        value = self._value.strip()

        # Допустимо: 'а' '2', '5а', '12A', '3Б'
        pattern = r"^[0-9]+[A-Za-zА-Яа-я]?$|^[A-Za-zА-Яа-я]$"
        if not re.match(pattern, value):
            raise InvalidBuildingBlockException(value=value)


class AuditoriumValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        value = self._value.strip()

        # Допустимо: '2', '5а', '12A', '3Б'
        pattern = r"^[0-9]+[A-Za-zА-Яа-я]?$"
        if not re.match(pattern, value):
            raise InvalidAuditoriumException(value=value)