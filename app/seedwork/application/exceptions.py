from abc import ABC, abstractmethod

from seedwork.exceptions import AppException


class ApplicationException(
    AppException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Application Exception"