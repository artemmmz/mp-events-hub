from dataclasses import dataclass
from uuid import UUID

from seedwork.infra.exception import InfraException


class MinioException(InfraException):
    @property
    def message(self) -> str:
        return "Minio exception"


@dataclass
class ContentNotExistException(MinioException):
    content_uid: UUID

    @property
    def message(self) -> str:
        return fr"Content {self.content_uid} not exist"