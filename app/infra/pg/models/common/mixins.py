from datetime import datetime, timezone
from uuid import UUID

from uuid_utils import uuid7
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UidPkMixin:
    uid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        server_default=func.now(),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(tz=timezone.utc),
        server_onupdate=func.now(),
    )


class IsEnabledMixin:
    enabled: Mapped[bool] = mapped_column(default=True, server_default="true")