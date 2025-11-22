from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from modules.auth.application.interface.dm import IRoleDm
from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.infra.dm.role import RoleAlchemyDm
from modules.auth.infra.repository.user import UserAlchemyRepository


class RepositoryAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
        mapper: UserMapper,
        role_dm: IRoleDm,
    ) -> IUserRepository:
        return UserAlchemyRepository(
            _session=session,
            _mapper=mapper,
            _role_dm=role_dm,
        )


class DMAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def role(
        self,
        session: AsyncSession,
    ) -> IRoleDm:
        return RoleAlchemyDm(_session=session)