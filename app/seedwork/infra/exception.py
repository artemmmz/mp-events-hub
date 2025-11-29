from abc import ABC, abstractmethod

from seedwork.exceptions import AppException


class InfraException(
    AppException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Base Infra Exception"