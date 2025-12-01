from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from seedwork.infra.pg.models.role import RoleOrm


from seedwork.infra.pg.models.common import (
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
)

class UserAuthOrm(
    BaseOrm,
    UidPkMixin,
    UpdatedAtMixin,
    CreatedAtMixin,
):
    __tablename__ = "users_auth"

    name: Mapped[str]
    second_name: Mapped[str]
    group_number: Mapped[str]
    email: Mapped[str] = mapped_column(index=True)
    hash_password: Mapped[bytes]
    email_confirm: Mapped[bool]

    role: Mapped["RoleOrm"] = relationship(back_populates="auth_users")

    role_uid: Mapped[UUID] = mapped_column(ForeignKey("roles.uid"))
