from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from seedwork.infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
)

if TYPE_CHECKING:
    from modules.auth.infra.pg.models.user import UserAuthOrm as UserAuthOrm
    from modules.event.infra.pg.models.user import UserEventOrm as UserEventOrm


class RoleOrm(
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)

    auth_users: Mapped[list["UserAuthOrm"]] = relationship(back_populates="role")
    event_users: Mapped[list["UserEventOrm"]] = relationship(back_populates="role")
