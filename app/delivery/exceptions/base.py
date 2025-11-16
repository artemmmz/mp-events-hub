from abc import (
    ABC,
    abstractmethod,
)

from seedwork.exceptions import AppException


class DeliveryException(
    AppException,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Presentation exception"