from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from seedwork.infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)


class EventRegistrationOrm(
    BaseOrm,
    UidPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    __tablename__ = "a_events_users"

    user_uid: Mapped[UUID] = mapped_column(
        ForeignKey("users_event.uid"),
        primary_key=True,
    )
    event_uid: Mapped[UUID] = mapped_column(
        ForeignKey(
            "events.uid",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )