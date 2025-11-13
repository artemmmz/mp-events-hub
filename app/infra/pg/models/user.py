from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from infra.pg.models.role import RoleOrm


from infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
)

class UserOrm(
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
):
    __tablename__ = "users"

    aggregate_id: Mapped[UUID]
    name: Mapped[str]
    second_name: Mapped[str]
    group_number: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[bytes]

    role: Mapped["RoleOrm"] = relationship(back_populates="user")

    role_uid: Mapped[UUID] = mapped_column(ForeignKey("roles.uid"))
