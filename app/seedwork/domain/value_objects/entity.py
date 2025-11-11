from dataclasses import dataclass
from typing import Any

from seedwork.domain.value_objects.base import BaseSimpleValueObject


@dataclass(
    frozen=True,
    slots=True,
)
class EntityIdValue(BaseSimpleValueObject[Any]):
    def validate(self) -> None:
        super().validate()
