from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BusinessRule(ABC):
    """This is a base class for implementing domain rules"""
    __message: str = field(default="Business rule is broken", init=False)

    def get_message(self) -> str:
        return self.__message

    @abstractmethod
    async def is_broken(self, *args: Any, **kwargs: Any) -> bool:
        ...
