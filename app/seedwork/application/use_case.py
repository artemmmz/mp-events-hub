from abc import ABC, abstractmethod
from typing import Generic, TypeVar


UCommand = TypeVar("UCommand")
UResult = TypeVar("UResult")


class UseCase(
    Generic[_UCommand, UResult],
    ABC,
):
    @abstractmethod
    def act(self, command: _UCommand) -> UResult:
        ...