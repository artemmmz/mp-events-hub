from dataclasses import dataclass

from modules.event.infra.pg.models.address import (
    AddressOrm,
    BuildingOrm,
)
from modules.event.domain.value_objects.address import (
    BuildingValue,
    AddressValue,
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


class BuildingMapper(BaseMapper):
    @staticmethod
    def to_orm(building: BuildingValue) -> BuildingOrm:
        return BuildingOrm(
            number=building.number.value,
            block=building.block.value,
            auditorium=building.auditorium.value,
        )