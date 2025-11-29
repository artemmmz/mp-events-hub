from dishka import Provider, Scope, provide

from bootstrap.settings import Settings
from modules.email.domain.services.sender import IEmailSender
from modules.email.infra.smtp.sender import SmtpEmailSender


class SmtpProvider(Provider):
    @provide(scope=Scope.APP)
    def sender(self, settings: Settings) -> IEmailSender:
        return SmtpEmailSender(
            smtp_host=settings.email.smtp_host,
            smtp_port=settings.email.smtp_port,
            username=settings.email.username,
            password=settings.email.password,
        )