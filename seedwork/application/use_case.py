from abc import ABC, abstractmethod
from typing import Generic, TypeVar


_UCommand = TypeVar("_UCommand")
_UResult = TypeVar("_UResult")


class UseCase(
    Generic[_UCommand, _UResult],
    ABC,
):
    @abstractmethod
    def act(self, command: _UCommand) -> _UResult:
        ...