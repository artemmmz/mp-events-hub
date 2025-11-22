from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider

from bootstrap.ioc.providers.bootstrap import(
    SettingProvider,
)
from bootstrap.ioc.providers.infra import (
    AlchemyProvider,
)
from bootstrap.ioc.providers.modules.auth import (
    RulesAuthProvider,
    RepositoryAuthProvider,
    MapperAuthProvider,
    ServiceAuthProvider,
    UseCaseAuthProvider,
    DMAuthProvider,
)
from bootstrap.ioc.providers.seedwork.infra import (
    TransactionManagerProvider,
)


DEV_PROVIDERS: list[Provider] = [
    SettingProvider(),
    AlchemyProvider(),
    RulesAuthProvider(),
    RepositoryAuthProvider(),
    MapperAuthProvider(),
    ServiceAuthProvider(),
    UseCaseAuthProvider(),
    DMAuthProvider(),
    TransactionManagerProvider(),
    FastapiProvider(),
]


def get_container() -> AsyncContainer:
    container: AsyncContainer = make_async_container(*DEV_PROVIDERS)

    return container

