from dataclasses import dataclass
from enum import Enum

from seedwork.domain.value_objects.common.base import BaseSimpleValueObject
from seedwork.domain.value_objects.exceptions import MediaTypeNotExistException


class MediaType(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    MP4 = "video/mp4"


@dataclass(frozen=True)
class MediaTypeValue(BaseSimpleValueObject[str, MediaType]):
    def validate(self) -> None:
        try:
            MediaType(self.value)
        except ValueError:
            raise MediaTypeNotExistException(media_type=self._value)

    def as_generic_type(self) -> MediaType:
        media_type = MediaType(self.value)
        return media_type