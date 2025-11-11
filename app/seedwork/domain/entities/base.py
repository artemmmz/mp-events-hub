from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)

from uuid_utils import uuid7

from seedwork.domain.value_objects.common.entity import EntityIdValue


@dataclass(
    kw_only=True,
    slots=True,
)
class Entity(ABC):
    id: EntityIdValue = field(
        default_factory=uuid7,
        repr=False,
    )

    @property
    def get_id(self) -> EntityIdValue:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id.get_value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            raise NotImplementedError

        return self.id == other.id


@dataclass(
    kw_only=True,
    slots=True,
)
class TimestampEntity(
    Entity,
    ABC,
):
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def get_created_time(self) -> datetime:
        return self._created_at

    @property
    def get_updated_time(self) -> datetime:
        return self._updated_at

    def _touch(self) -> None:
        self._updated_at = datetime.now(tz=timezone.utc)