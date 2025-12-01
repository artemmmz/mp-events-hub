from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from modules.event.domain.aggregate.exceptions import AddressFormatException
from modules.event.domain.value_objects.address import (
    AddressValue,
    CityValue,
    StreetValue,
    BuildingValue,
    BuildingNumberValue,
    BuildingBlockValue,
    AuditoriumValue,
)
from modules.event.domain.value_objects.event import (
    TitleValue,
    ScheduledAtValue,
    DescriptionValue,
)
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.common.entity import EntityIdValue


@dataclass
class Event(BaseAggregate):
    created_by_user_id: EntityIdValue
    title: TitleValue
    scheduled_at: ScheduledAtValue
    address: AddressValue | None
    description: DescriptionValue

    @classmethod
    def create(
        cls,
        created_by_user_id: UUID,
        title: str,
        scheduled_at: datetime,
        description: str,
        city: str,
        street: str,
        building_number: int,
        block: str | None,
        auditorium: str | None,
    ) -> "Event":
        address_vo: AddressValue | None = None

        if city and street and building_number is not None:
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

        if 3 > sum(v is not None for v in [city, street, building_number]) > 0:
            raise AddressFormatException(
                city=city,
                street=street,
                building_number=building_number,
            )

        return Event(
            created_by_user_id=EntityIdValue(created_by_user_id),
            title=TitleValue(title),
            scheduled_at=ScheduledAtValue(scheduled_at),
            address=address_vo,
            description=DescriptionValue(description),
        )
