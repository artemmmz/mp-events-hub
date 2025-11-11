from dataclasses import dataclass

import bcrypt

from seedwork.domain.aggregate.base import BaseAggregate
from seedwork.domain.value_objects.user import NameValue, GroupNumberValue, EmailValue


@dataclass
class User(BaseAggregate):
    name: NameValue
    second_name: NameValue
    group_number: GroupNumberValue
    email: EmailValue
    hash_password: bytes

    @classmethod
    def create(
        cls,
        name: str,
        second_name: str,
        group_number: str,
        email: str,
        password: str,
    ) -> "User":
        hash_password: bytes = cls._hash_password(password=password)

        return User(
            name=NameValue(_value=name),
            second_name=NameValue(_value=second_name),
            group_number=GroupNumberValue(_value=group_number),
            email=EmailValue(_value=email),
            hash_password=hash_password,
        )

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=self.hash_password,
        )

    @staticmethod
    def _hash_password(password: str) -> bytes:
        return bcrypt.hashpw(
            password=password.encode('utf-8'),
            salt=bcrypt.gensalt(),
        )