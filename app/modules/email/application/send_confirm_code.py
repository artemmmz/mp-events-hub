from dataclasses import dataclass

from modules.email.domain.aggregate.email import Email
from modules.email.domain.services.sender import IEmailSender
from seedwork.application.use_case import BaseUseCase


@dataclass
class SendConfirmCodeCommand:
    email: str
    confirm_code: str
    subject: str


@dataclass
class SendConfirmCodeUseCase(BaseUseCase):
    _email_sender: IEmailSender

    async def act(self, command: SendConfirmCodeCommand) -> None:
        email: Email = Email.create(
            to=command.email,
            subject=command.subject,
            body=command.confirm_code,
        )

        await self._email_sender.send(email=email)