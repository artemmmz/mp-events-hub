from dataclasses import dataclass

from seedwork.application.exceptions import ApplicationException


@dataclass
class ConfirmCodeNotFoundException(ApplicationException):
    @property
    def message(self) -> str:
        return "Confirmation code not found for user"