from modules.event.application.validators.exceptions import (
    ContentTypeEmptyException,
    ImageInvalidSizeException,
    ImageSizeTooLargeException,
    ImageSizeTooSmallException,
    ContentTypeNotAllowedException,
)
from seedwork.application.validators.base import BaseValidator


MIN_WIDTH = 400
MIN_HEIGHT = 400
MAX_WIDTH = 4000
MAX_HEIGHT = 4000


class EventImageValidator(BaseValidator):
    async def validate(
        self,
        content_type: str,
        height: int,
        wight: int,
    ) -> None:
        allowed_content_types = {
            "image/jpeg",
            "image/png",
        }

        if not content_type:
            raise ContentTypeEmptyException()

        if height <= 0 or wight <= 0:
            raise ImageInvalidSizeException(
                width=wight,
                height=height,
            )

        if content_type not in allowed_content_types:
            raise ContentTypeNotAllowedException(content_type=content_type)

        if wight < MIN_WIDTH or height < MIN_HEIGHT:
            raise ImageSizeTooSmallException(
                width=wight,
                height=height,
                min_width=MIN_WIDTH,
                min_height=MIN_HEIGHT,
            )

        if wight > MAX_WIDTH or height > MAX_HEIGHT:
            raise ImageSizeTooLargeException(
                width=wight,
                height=height,
                max_width=MAX_WIDTH,
                max_height=MAX_HEIGHT,
            )