from seedwork.domain.aggregate.exceptions import AggregateException


class InvalidConfirmCodeException(AggregateException):
    def message(self) -> str:
        return "Invalid confirm code"
