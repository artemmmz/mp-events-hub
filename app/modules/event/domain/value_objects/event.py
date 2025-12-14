from datetime import datetime

from seedwork.domain.value_objects.common.base import (
    BaseSimpleValueObject,
)
from seedwork.domain.value_objects.validators.lens import len_validate


class TitleValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=50,
            min_len=3,
        )


class ScheduledAtValue(BaseSimpleValueObject[datetime, datetime]):
    def validate(self) -> None:
        pass


class DescriptionValue(BaseSimpleValueObject[str, str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=1000,
            min_len=3,
        )