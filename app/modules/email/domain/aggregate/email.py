from dataclasses import dataclass

from modules.email.domain.value_objects.email import SubjectValue, BodyValue
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.user import EmailValue


@dataclass
class Email(BaseAggregate):
    to: EmailValue
    subject: SubjectValue
    body: BodyValue

    @classmethod
    def create(
        cls,
        to: str,
        subject: str,
        body: str,
    ) -> "Email":
        return Email(
            to=EmailValue(_value=to),
            subject=SubjectValue(_value=subject),
            body=BodyValue(_value=body),
        )