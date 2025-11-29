from dataclasses import dataclass
from datetime import datetime

from modules.events.domain.value_objects.address import (
    AddressValue,
    CityValue,
    StreetValue,
    BuildingValue,
    BuildingNumberValue,
    BuildingBlockValue,
    AuditoriumValue,
)
from modules.events.domain.value_objects.event import (
    TitleValue,
    ScheduledAtValue,
    DescriptionValue,
)
from seedwork.domain.aggregate.base import BaseAggregate


@dataclass
class Event(BaseAggregate):
    title: TitleValue
    scheduled_at: ScheduledAtValue
    address: AddressValue
    description: DescriptionValue

    @classmethod
    def create(
        cls,
        title: str,
        scheduled_at: datetime,
        description: str,
        city: str,
        street: str,
        building_number: int,
        block: str | None,
        auditorium: str | None,
    ) -> "Event":
        block_vo: BuildingBlockValue | None = (
            BuildingBlockValue(block)) if block else None

        auditorium_vo: AuditoriumValue | None = (
            AuditoriumValue(auditorium)) if auditorium else None

        building_vo = BuildingValue(
            number=BuildingNumberValue(_value=building_number),
            block=block_vo,
            auditorium=auditorium_vo,
        )

        address_vo = AddressValue(
            city=CityValue(_value=city),
            street=StreetValue(_value=street),
            building=building_vo,
        )

        return Event(
            title=TitleValue(_value=title),
            scheduled_at=ScheduledAtValue(_value=scheduled_at),
            address=address_vo,
            description=DescriptionValue(_value=description),
        )

