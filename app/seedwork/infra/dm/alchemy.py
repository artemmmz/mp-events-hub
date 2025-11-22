from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.infra.dm.base import BaseDataMapper


@dataclass
class BaseAlchemyDataMapper(BaseDataMapper):
    _session: AsyncSession
