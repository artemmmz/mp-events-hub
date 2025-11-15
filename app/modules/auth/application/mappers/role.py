from modules.auth.domain.value_object.roles import RoleValue
from infra.pg.models.role import RoleOrm
from seedwork.application.mapper import BaseMapper


class RoleMapper(BaseMapper):
    @staticmethod
    def to_orm(role: RoleValue) -> RoleOrm:
        return RoleOrm(name=role.value)