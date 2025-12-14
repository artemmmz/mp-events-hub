import asyncio
from dataclasses import dataclass
from io import BytesIO

from PIL.ImageFile import ImageFile
from PIL import Image

from seedwork.infra.s3.support_obj import AsyncReadable


@dataclass
class ImageMetadataSchema:
    width: int
    height: int
    content_type: str


class ImageMetadataService:
    """Работает с image and gif"""

    async def get(self, file: AsyncReadable) -> ImageMetadataSchema:
        header: bytes = await self._get_header(file=file)
        image: ImageFile = await asyncio.to_thread(
            self._get_image,
            header=header,
        )

        width, height = image.size
        content_type: str = image.format

        await file.seek(0)

        resolution = ImageMetadataSchema(
            width=width,
            height=height,
            content_type=content_type,
        )
        return resolution

    @staticmethod
    def _get_image(header: bytes) -> ImageFile:
        image = Image.open(BytesIO(header)) # type: ignore[arg-type]
        return image

    @staticmethod
    async def _get_header(file: AsyncReadable) -> bytes:
        header: bytes = await file.read(65536)
        return header
