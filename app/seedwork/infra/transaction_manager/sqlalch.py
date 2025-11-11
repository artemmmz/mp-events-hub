from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SQLAlchemyTransactionManager:
    _session: AsyncSession.add

    async def add(self, instance: Any) -> None:
        self._session.add(instance)

    async def add_all(self, instances: Sequence[Any]) -> None:
        self._session.add_all(instances)

    async def commit(self) -> None:
        await self._session.commit()

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, instance: Any) -> None:
        await self._session.refresh(instance)