from typing import Protocol, Any, Sequence


class ITransactionManager(Protocol):
    async def add(self, instance: Any) -> None:
        """Добавить одну сущность в текущую транзакцию."""

    async def add_all(self, instances: Sequence[Any]) -> None:
        """Добавить несколько сущностей в текущую транзакцию."""

    async def commit(self) -> None:
        """Зафиксировать транзакцию."""

    async def flush(self) -> None:
        """Сбросить изменения в БД без коммита."""

    async def refresh(self, instance: Any) -> None:
        """Обновить данные объекта из БД."""