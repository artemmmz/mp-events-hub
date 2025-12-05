from abc import ABC, abstractmethod

from modules.event.domain.aggregate.event import Event
from seedwork.domain.repository import BaseRepository
from seedwork.domain.value_objects.common.entity import EntityIdValue


class IEventRepository(
    BaseRepository,
    ABC,
):
    @abstractmethod
    async def create(self, event: Event) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, _id: EntityIdValue) -> Event:
        ...

    @abstractmethod
    async def delete(self, _id: EntityIdValue) -> None:
        ...

    @abstractmethod
    async def update(self, event: Event) -> Event:
        ...