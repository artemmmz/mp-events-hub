from typing import  Protocol, AsyncGenerator


class AsyncReadable(Protocol):
    async def read(self, n: int = -1) -> bytes:
        ...

    async def seek(self, offset: int) -> None:
        ...


class AsyncFileStreamer:
    """
    Обёртка для асинхронного file-like объекта.
    Позволяет стримить в S3 через AsyncGenerator[bytes, None].
    """
    def __init__(
        self,
        file_obj: AsyncReadable,
        chunk_size: int = 1024*1024 * 5,
    ) -> None:
        self.file_obj = file_obj
        self.chunk_size = chunk_size

    async def __aiter__(self) -> AsyncGenerator[bytes, None]:
        while True:
            chunk = await self.file_obj.read(self.chunk_size)
            if not chunk:
                break
            yield chunk

    def to_generator(self) -> AsyncGenerator[bytes, None]:
        return self.__aiter__()