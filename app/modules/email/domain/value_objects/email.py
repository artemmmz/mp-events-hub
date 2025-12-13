from seedwork.domain.value_objects.common.base import BaseSimpleValueObject
from seedwork.domain.value_objects.common.exceptions import (
    EmptyValueException,
    ValueTooLongException,
)


class SubjectValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        if len(self._value.strip()) == 0:
            raise EmptyValueException()

        if len(self._value) > 255:
            raise ValueTooLongException(
                _max_len=255,
                current_len=len(self._value),
            )


class BodyValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        if len(self._value.strip()) == 0:
            raise EmptyValueException()