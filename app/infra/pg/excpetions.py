from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from seedwork.infra.exception import InfraException


class PgException(InfraException):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Pg Exception"


@dataclass
class MissingRequiredFieldException(PgException):
    required_field: str | Iterable

    @property
    def message(self) -> str:
        if isinstance(self.required_field, str):
            fields_str = self.required_field
        elif isinstance(self.required_field, Iterable):
            fields_str = ", ".join(str(f) for f in self.required_field)
        else:
            fields_str = str(self.required_field)

        return fr"Missing required field(s): {fields_str}"
