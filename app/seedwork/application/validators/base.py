from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from seedwork.application.exceptions import ApplicationException


@dataclass
class BaseValidator(ABC):
    __message: str = field(default="Validate obj is broken", init=False)

    def get_message(self) -> str:
        return self.__message

    @abstractmethod
    async def validate(self, *args: Any, **kwargs: Any) -> None:
        ...


@dataclass
class BaseValidatorException(
    ApplicationException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "BaseValidatorException"