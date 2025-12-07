import asyncio

import pytest
from dishka import AsyncContainer

from seedwork.application.interface.dm.sql.roles import IRoleDm
from seedwork.domain.value_objects.role import RoleValue
from seedwork.infra.pg.models import RoleOrm
from seedwork.infra.transaction_manager.base import ITransactionManager


@pytest.fixture(scope="session", autouse=True)
async def fill_roles(
    ioc_container: AsyncContainer,
) -> None:
    async with ioc_container() as cont:
        role_dm: IRoleDm = await cont.get(IRoleDm)
        transaction_manager: ITransactionManager = await cont.get(ITransactionManager)

        user_role_orm = RoleOrm(
            name=RoleValue.USER.value,
        )
        organizer_role_orm = RoleOrm(
            name=RoleValue.ORGANIZER.value,
        )
        admin_role_orm = RoleOrm(
            name=RoleValue.ADMIN.value,
        )

        roles: list[RoleOrm] = [
            user_role_orm,
            organizer_role_orm,
            admin_role_orm,
        ]

        tasks = [role_dm.create(role_orm=role_orm) for role_orm in roles]

        await asyncio.gather(*tasks)

        await transaction_manager.commit()