from abc import ABC, abstractmethod

from modules.event.domain.aggregate.event import Event
from seedwork.domain.repository import BaseRepository


class IEventRepository(
    BaseRepository,
    ABC,
):
    @abstractmethod
    async def create(self, event: Event) -> None:
        ...