from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from modules.event.domain.repository.event import IEventRepository
from modules.event.domain.repository.user import IUserRepository
from modules.event.infra.dm.user import IUserDm, UserAlchemyDm
from modules.event.infra.mappers.address import AddressMapper, BuildingMapper
from modules.event.infra.mappers.event import EventMapper
from modules.event.infra.mappers.user import UserMapper
from modules.event.infra.repository.event import EventAlchemyRepository
from modules.event.infra.repository.user import UserAlchemyRepository
from seedwork.application.interface.dm.sql.roles import IRoleDm


class DmEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
    ) -> IUserDm:
        return UserAlchemyDm(_session=session)


class RepositoryEventProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user(
        self,
        session: AsyncSession,
        role_dm: IRoleDm,
        mapper: UserMapper,
    ) -> IUserRepository:
        return UserAlchemyRepository(
            _session=session,
            _role_dm=role_dm,
            _mapper=mapper,
        )

    @provide
    def event(
        self,
        session: AsyncSession,
        mapper: EventMapper,
        user_dm: IUserDm,
    ) -> IEventRepository:
        return EventAlchemyRepository(
            _session=session,
            _mapper=mapper,
            _user_dm=user_dm,
        )


class MapperEventProvider(Provider):
    scope = Scope.APP

    @provide
    def user(self) -> UserMapper:
        return UserMapper()

    @provide
    def event(
        self,
        address_mapper: AddressMapper,
    ) -> EventMapper:
        return EventMapper(
            _address_mapper=address_mapper,
        )

    @provide
    def address(
        self,
        building_mapper: BuildingMapper,
    ) -> AddressMapper:
        return AddressMapper(
            _building_mapper=building_mapper,
        )

    @provide
    def building(self) -> BuildingMapper:
        return BuildingMapper()