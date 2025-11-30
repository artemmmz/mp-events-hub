from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
)

if TYPE_CHECKING:
    from infra.pg.models.user import UserOrm


class RoleOrm(
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["UserOrm"]] = relationship(back_populates="role")
