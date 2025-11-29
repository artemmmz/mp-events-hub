from dishka import Provider, Scope, provide

from modules.email.application.send_confirm_code import SendConfirmCodeUseCase
from modules.email.domain.services.sender import IEmailSender


class InfraEmailUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def send_confirm_code(
        self,
        email_sender: IEmailSender,
    ) -> SendConfirmCodeUseCase:
        return SendConfirmCodeUseCase(
            _email_sender=email_sender,
        )