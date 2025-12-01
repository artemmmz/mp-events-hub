from dataclasses import dataclass

from modules.event.infra.pg.models.address import AddressOrm
from modules.event.infra.pg.models.event import EventOrm
from modules.event.domain.aggregate.event import Event
from modules.event.infra.mappers.address import AddressMapper
from seedwork.domain.mapper import BaseMapper


@dataclass
class EventMapper(BaseMapper):
    _address_mapper: AddressMapper

    def to_orm(self, event: Event) -> EventOrm:
        address_orm: AddressOrm | None = None

        if event.address:
            address_orm = self._address_mapper.to_orm(address=event.address)

        return EventOrm(
            uid=event.id.value,
            title=event.title.value,
            description=event.description.value,
            scheduled_at=event.scheduled_at.value,
            created_by_user_id=event.created_by_user_id.value,
            address=address_orm,
        )