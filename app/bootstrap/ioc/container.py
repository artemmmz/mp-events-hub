from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider

from bootstrap.ioc.providers.infra import (
    AlchemyProvider,
)
from bootstrap.ioc.providers.modules.auth import (
    RulesAuthProvider,
    RepositoryAuthProvider,
    MapperAuthProvider,
    ServiceAuthProvider,
    UseCaseAuthProvider,
)


DEV_PROVIDERS: list[Provider] = [
    AlchemyProvider(),
    RulesAuthProvider,
    RepositoryAuthProvider,
    MapperAuthProvider,
    ServiceAuthProvider,
    UseCaseAuthProvider,
    FastapiProvider(),
]


def get_container() -> AsyncContainer:
    container: AsyncContainer = make_async_container(*DEV_PROVIDERS)

    return container

