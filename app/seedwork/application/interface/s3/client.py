from typing import Protocol, AsyncGenerator
from uuid import UUID

from seedwork.domain.value_objects.content_types import ContentType
from seedwork.domain.value_objects.s3 import Bucket


class IS3Client(Protocol):
    async def upload_stream(
        self,
        file: AsyncGenerator[bytes, None],
        key: UUID,
        bucket: Bucket,
        content_type: ContentType,
    ) -> UUID:
        ...

    async def delete(
        self,
        key: UUID,
        bucket: Bucket,
    ) -> None:
        ...