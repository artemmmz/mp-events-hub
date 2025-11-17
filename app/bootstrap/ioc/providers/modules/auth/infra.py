from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from modules.auth.application.mappers.user import UserMapper
from modules.auth.domain.repository.user import IUserRepository
from modules.auth.infra.repository.user import UserAlchemyRepository


class RepositoryAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
        mapper: UserMapper,

    ) -> IUserRepository:
        return UserAlchemyRepository(
            _session=session,
            _mapper=mapper,
        )