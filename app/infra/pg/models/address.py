from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
)

if TYPE_CHECKING:
    from infra.pg.models.event import EventOrm


class AddressOrm(
    BaseOrm,
    UidPkMixin,
):
    __tablename__ = "addresses"

    city: Mapped[str]
    street: Mapped[str]
    event_uid: Mapped[UUID] = mapped_column(
        ForeignKey("events.uid"),
    )

    building: Mapped["BuildingOrm"] = relationship(
        back_populates="address",
    )
    event: Mapped["EventOrm"] = relationship(
        back_populates="address",
    )


class BuildingOrm(
    BaseOrm,
    UidPkMixin,
):
    __tablename__ = "buildings"

    number: Mapped[int]
    block: Mapped[str | None]
    auditorium: Mapped[str | None]

    address_uid: Mapped[UUID] = mapped_column(
        ForeignKey("addresses.uid"),
    )

    address: Mapped["AddressOrm"] = relationship(
        back_populates="building",
    )
