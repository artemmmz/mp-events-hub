from enum import Enum
from uuid import UUID

from seedwork.domain.value_objects.common.base import BaseSimpleValueObject


class S3IdValue(BaseSimpleValueObject[UUID, UUID]):
    pass


class Bucket(Enum):
    IMAGE = "image"
    GIF = "gif"
    VIDEO = "video"