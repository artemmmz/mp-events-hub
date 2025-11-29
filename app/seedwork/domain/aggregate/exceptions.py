from abc import ABC, abstractmethod

from seedwork.domain.exception import DomainException


class AggregateException(
    DomainException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Aggregate Exception"