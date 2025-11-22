from abc import ABC, abstractmethod


class AppException(
    Exception,
    ABC,
):
    @property
    @abstractmethod
    def message(self) -> str:
        return "App exception"