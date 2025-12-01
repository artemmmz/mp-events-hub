from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from modules.auth.application.interface.dm.kvalue.user import IUserKvDm
from seedwork.application.interface.dm.sql.roles import IRoleDm
from modules.auth.application.interface.dm.sql.user import IUserDm
from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.repository.user import IUserRepository
from seedwork.infra.dm.role import RoleAlchemyDm
from modules.auth.infra.dm.alchemy.user import UserAlchemyDm
from modules.auth.infra.dm.redis.user import UserRedisDm
from modules.auth.infra.repository.user import UserAlchemyRepository


class RepositoryAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
        mapper: UserMapper,
        role_dm: IRoleDm,
        user_dm: IUserDm,
    ) -> IUserRepository:
        return UserAlchemyRepository(
            _session=session,
            _mapper=mapper,
            _role_dm=role_dm,
            _user_dm=user_dm,
        )


class DmAlchemyAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def role(
        self,
        session: AsyncSession,
    ) -> IRoleDm:
        return RoleAlchemyDm(_session=session)

    @provide
    def user(
        self,
        session: AsyncSession,
    ) -> IUserDm:
        return UserAlchemyDm(_session=session)


class DmRedisAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        redis: Redis,
    ) -> IUserKvDm:
        return UserRedisDm(_redis=redis)