from dataclasses import dataclass
from random import randint

import bcrypt

from modules.auth.domain.aggregate.exception import (
    InvalidConfirmCodeException,
    InvalidEmailException,
)
from seedwork.domain.events.auth import (
    RequestedRegistrationUserEvent,
    ConfirmRegistrationUserEvent,
    RequestResetPasswordEvent,
)
from modules.auth.domain.value_object.confirm_code import ConfirmCodeValue
from seedwork.domain.value_objects.role import RoleValue
from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.user import (
    NameValue,
    GroupNumberValue,
    EmailValue,
)


@dataclass
class User(BaseAggregate):
    name: NameValue
    second_name: NameValue
    group_number: GroupNumberValue
    email: EmailValue
    hash_password: bytes
    role: RoleValue
    email_confirm: bool

    @classmethod
    def create(
        cls,
        name: str,
        second_name: str,
        group_number: str,
        email: str,
        password: str | bytes,
        role: RoleValue,
        email_confirm: bool,
    ) -> "User":

        if isinstance(password, str):
            hash_password: bytes = cls._hash_password(password=password)
        else:
            hash_password = password

        return User(
            name=NameValue(_value=name),
            second_name=NameValue(_value=second_name),
            group_number=GroupNumberValue(_value=group_number),
            email=EmailValue(_value=email),
            hash_password=hash_password,
            role=role,
            email_confirm=email_confirm,
        )

    def unconfirmed_registration(self) -> ConfirmCodeValue:
        confirm_code: str = str(randint(10_000, 99_999))
        event = RequestedRegistrationUserEvent(
            email=self.email.value,
            confirm_code=confirm_code,
        )

        self.register_event(event=event)

        return ConfirmCodeValue(_value=confirm_code)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=self.hash_password,
        )

    def confirm_register(
        self,
        input_code: ConfirmCodeValue,
        stored_code: ConfirmCodeValue,
    ) -> None:
        if input_code != stored_code:
            raise InvalidConfirmCodeException()

        self.email_confirm = True

        event = ConfirmRegistrationUserEvent(
            user_id=self.id.value,
            role=self.role.value,
        )

        self.register_event(event)

    def reset_password_request(
        self,
        email: EmailValue,
    ) -> ConfirmCodeValue:
        confirm_code: str = str(randint(10_000, 99_999))

        if email != self.email:
            raise InvalidEmailException()

        event = RequestResetPasswordEvent(
            email=email.value,
            confirm_code=confirm_code,
        )

        self.register_event(event=event)

        return ConfirmCodeValue(confirm_code)

    def reset_password(
        self,
        new_password: str,
        input_code: ConfirmCodeValue,
        stored_code: ConfirmCodeValue,
    ) -> None:
        if input_code != stored_code:
            raise InvalidConfirmCodeException()

        self.hash_password = self._hash_password(new_password)

    @staticmethod
    def _hash_password(password: str) -> bytes:
        return bcrypt.hashpw(
            password=password.encode('utf-8'),
            salt=bcrypt.gensalt(),
        )