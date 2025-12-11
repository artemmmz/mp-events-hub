from seedwork.domain.aggregate.exceptions import AggregateException


class InvalidConfirmCodeException(AggregateException):
    def message(self) -> str:
        return "Invalid confirm code"


class InvalidEmailException(AggregateException):
    def message(self) -> str:
        return "Email does not match the user's email"