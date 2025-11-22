from abc import ABC, abstractmethod

from seedwork.exceptions import AppException


class DomainException(
    AppException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Domain exception"