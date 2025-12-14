from dataclasses import dataclass

from seedwork.application.validators.base import BaseValidatorException


@dataclass
class ContentTypeEmptyException(BaseValidatorException):
    @property
    def message(self) -> str:
        return "Тип содержимого изображения не указан"


@dataclass
class ContentTypeNotAllowedException(BaseValidatorException):
    content_type: str

    @property
    def message(self) -> str:
        return f"Тип содержимого '{self.content_type}' не разрешен"


@dataclass
class ImageSizeTooSmallException(BaseValidatorException):
    width: int
    height: int
    min_width: int
    min_height: int

    @property
    def message(self) -> str:
        return (
            f"Размер изображения слишком мал: "
            f"{self.width}x{self.height}, минимум {self.min_width}x{self.min_height}"
        )


@dataclass
class ImageSizeTooLargeException(BaseValidatorException):
    width: int
    height: int
    max_width: int
    max_height: int

    @property
    def message(self) -> str:
        return (
            f"Размер изображения слишком велик: "
            f"{self.width}x{self.height}, максимум {self.max_width}x{self.max_height}"
        )


@dataclass
class ImageInvalidSizeException(BaseValidatorException):
    width: int
    height: int

    @property
    def message(self) -> str:
        return f"Некорректный размер изображения: {self.width}x{self.height}"