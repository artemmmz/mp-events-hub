from abc import ABC, abstractmethod

from modules.email.domain.aggregate.email import Email


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, email: Email) -> None:
        ...