from datetime import datetime, timezone

from modules.events.domain.value_objects.exceptions import EventInPastException
from seedwork.domain.value_objects.common.base import (
    BaseSimpleValueObject,
)
from seedwork.domain.value_objects.validators.lens import len_validate


class TitleValue(BaseSimpleValueObject[str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=50,
            min_len=3,
        )


class ScheduledAtValue(BaseSimpleValueObject[datetime]):
    def validate(self) -> None:
        dt_now: datetime = datetime.now(tz=timezone.utc)

        if self.value < dt_now:
            raise EventInPastException(value=str(self.value))


class DescriptionValue(BaseSimpleValueObject[str]):
    def validate(self) -> None:
        len_validate(
            value=self._value,
            max_len=1000,
            min_len=3,
        )