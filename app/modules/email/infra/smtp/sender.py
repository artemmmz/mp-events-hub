import aiosmtplib
from dataclasses import dataclass
from email.mime.text import MIMEText

from modules.email.domain.aggregate.email import Email
from modules.email.domain.services.sender import IEmailSender


@dataclass
class SmtpEmailSender(IEmailSender):
    smtp_host: str
    smtp_port: int
    username: str
    password: str

    async def send(self, email: Email) -> None:
        body = email.body.value
        is_html = "<" in body and ">" in body

        if is_html:
            msg = MIMEText(body, "html")
        else:
            msg = MIMEText(body, "plain")

        msg['Subject'] = email.subject
        msg['From'] = self.username
        msg['To'] = email.to.value

        await aiosmtplib.send(
            msg,
            recipients=[email.to.value],
            hostname=self.smtp_host,
            port=self.smtp_port,
            start_tls=True,
            username=self.username,
            password=self.password,
        )