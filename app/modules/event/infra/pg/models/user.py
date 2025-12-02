from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seedwork.infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from seedwork.infra.pg.models.role import RoleOrm
    from modules.event.infra.pg.models import EventOrm


class UserEventOrm(
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    __tablename__ = "users_event"

    role_uid: Mapped[UUID] = mapped_column(
        ForeignKey("roles.uid"),
    )

    role: Mapped["RoleOrm"] = relationship(
        back_populates="event_users",
    )
    events_created: Mapped[list["EventOrm"]] = relationship(
        back_populates="created_by_user",
    )
    registered_events: Mapped[list["EventOrm"]] = relationship(
        back_populates="registered_users",
        secondary="a_events_users",
    )