from dataclasses import dataclass
from typing import Any

from seedwork.domain.value_objects.common.base import BaseSimpleValueObject


@dataclass(
    frozen=True,
    slots=True,
)
class EntityIdValue(BaseSimpleValueObject[Any]):
    pass