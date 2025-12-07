from typing import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from bootstrap.settings import Settings


class AlchemyProvider(Provider):
    def __init__(
        self,
        connection_string: str | None = None,
    ) -> None:
        super().__init__()
        self.connection_string: str | None = connection_string

    @provide(scope=Scope.APP)
    async def create_engine(
        self,
        settings: Settings,
    ) -> AsyncEngine:
        pg_url: str = settings.pg.postgres_url

        if self.connection_string:
            pg_url = self.connection_string

        engine: AsyncEngine = create_async_engine(
            url=pg_url,
            echo=False,
        )
        return engine

    @provide(scope=Scope.APP)
    async def create_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session