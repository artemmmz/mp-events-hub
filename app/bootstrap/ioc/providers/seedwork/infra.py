from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.infra.transaction_manager.base import ITransactionManager
from seedwork.infra.transaction_manager.sqlalch import SQLAlchemyTransactionManager


class TransactionManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def t_manager(self, session: AsyncSession) -> ITransactionManager:
        return SQLAlchemyTransactionManager(_session=session)