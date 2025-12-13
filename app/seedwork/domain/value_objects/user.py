import re

from seedwork.domain.value_objects.common.base import BaseSimpleValueObject
from seedwork.domain.value_objects.exceptions import (
    GroupNumberFormatException,
    EmailFormatException,
)
from seedwork.domain.value_objects.validators.lens import len_validate


class NameValue(
    BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=25,
            min_len=2,
        )


class GroupNumberValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        pattern = r"^\d{3}-\d{3}$"

        if not re.match(pattern, self._value):
            raise GroupNumberFormatException(group_number=self._value)


class EmailValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, self._value):
            raise EmailFormatException(self._value)