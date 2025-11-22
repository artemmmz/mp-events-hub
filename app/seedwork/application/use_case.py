from abc import ABC, abstractmethod
from typing import Generic, TypeVar


UCommand = TypeVar("UCommand")
UResult = TypeVar("UResult")


class BaseUseCase(
    Generic[UCommand, UResult],
    ABC,
):
    @abstractmethod
    def act(self, command: UCommand) -> UResult:
        ...