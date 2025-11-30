from dataclasses import dataclass

from seedwork.domain.aggregate.exceptions import AggregateException


@dataclass
class AddressFormatException(AggregateException):
    city: str
    street: str
    building_number: int

    @property
    def message(self) -> str:
        message = (
            f"Invalid address: city='{self.city}', street='{self.street}', building_number='{self.building_number}'. "
            "All three fields must be provided."
        )

        return message


@dataclass
class UserRoleNotAllowedException(AggregateException):
    role: str

    @property
    def message(self) -> str:
        return f"Пользователь с ролью '{self.role}' не может создавать событие."