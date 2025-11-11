from seedwork.domain.value_objects.common.base import ValueType
from seedwork.domain.value_objects.common.exceptions import (
    ValueTooLongException,
    ValueTooShortException,
)


def len_validate(
    value: ValueType,
    max_len: int,
    min_len:int,
) -> None:
    value_len: int = len(value)

    if value_len > max_len:
        raise ValueTooLongException(
            _max_len=max_len,
            current_len=value_len,
        )

    if value_len < min_len:
        raise ValueTooShortException(
            _min_len=min_len,
            current_len=value_len,
        )