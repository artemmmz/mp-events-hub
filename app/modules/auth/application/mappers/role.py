from seedwork.domain.value_objects.role import RoleValue
from seedwork.infra.pg.models.role import RoleOrm
from seedwork.domain.mapper import BaseMapper


class RoleMapper(BaseMapper):
    @staticmethod
    def to_orm(role: RoleValue) -> RoleOrm:
        return RoleOrm(name=role.value)