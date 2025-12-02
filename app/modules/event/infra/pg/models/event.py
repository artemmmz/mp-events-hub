from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seedwork.infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from modules.event.infra.pg.models import UserEventOrm, AddressOrm


class EventOrm(
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    __tablename__ = "events"

    title: Mapped[str]
    description: Mapped[str]
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    created_by_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users_event.uid"),
    )

    created_by_user: Mapped["UserEventOrm"] = relationship(
        back_populates="events_created",
    )
    address: Mapped[Optional["AddressOrm"]] = relationship(
        back_populates="event",
    )
    registered_users: Mapped[list["UserEventOrm"]] = relationship(
        back_populates="registered_events",
        secondary="a_events_users",
    )