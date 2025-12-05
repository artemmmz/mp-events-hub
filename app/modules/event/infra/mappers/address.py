from dataclasses import dataclass

from modules.event.infra.pg.models.address import (
    AddressOrm,
    BuildingOrm,
)
from modules.event.domain.value_objects.address import (
    BuildingValue,
    AddressValue, CityValue, StreetValue, BuildingBlockValue, BuildingNumberValue, AuditoriumValue,
)
from seedwork.domain.mapper import BaseMapper


@dataclass
class AddressMapper(BaseMapper):
    _building_mapper: "BuildingMapper"

    def to_orm(
        self,
        address: AddressValue,
    ) -> AddressOrm:
        building_orm: BuildingOrm = self._building_mapper.to_orm(address.building)

        return AddressOrm(
            city=address.city.value,
            street=address.street.value,
            building=building_orm,
        )

    def to_value_object(self, address_orm: AddressOrm) -> AddressValue:
        building_vo: BuildingValue = self._building_mapper.to_value_object(
            building_orm=address_orm.building,
        )

        return AddressValue(
            city=CityValue(address_orm.city),
            street=StreetValue(address_orm.street),
            building=building_vo,
        )

class BuildingMapper(BaseMapper):
    @staticmethod
    def to_orm(building: BuildingValue) -> BuildingOrm:
        block: str | None = building.block.value if building.block else None
        auditorium: str | None = building.auditorium.value if building.auditorium else None

        return BuildingOrm(
            number=building.number.value,
            block=block,
            auditorium=auditorium,
        )

    @staticmethod
    def to_value_object(building_orm: BuildingOrm) -> BuildingValue:
        block: BuildingBlockValue | None = None
        auditorium: AuditoriumValue | None = None

        if building_orm.block:
            block = BuildingBlockValue(building_orm.block)

        if building_orm.auditorium:
            auditorium = AuditoriumValue(building_orm.auditorium)

        return BuildingValue(
            number=BuildingNumberValue(building_orm.number),
            block=block,
            auditorium=auditorium,
        )