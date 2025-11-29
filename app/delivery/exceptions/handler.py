from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)

from seedwork.domain.value_objects.common.exceptions import ValueException
from seedwork.exceptions import AppException
from modules.auth.domain.rules.exceptions import (
    UserAlreadyExistsException,
    EmailAlreadyExistsException,
    UserNotFoundException,
    InvalidPasswordException,
)


exceptions_map: dict[type[AppException], int] = {
    AppException: HTTP_500_INTERNAL_SERVER_ERROR,
    UserAlreadyExistsException: HTTP_409_CONFLICT,
    EmailAlreadyExistsException: HTTP_409_CONFLICT,
    UserNotFoundException: HTTP_404_NOT_FOUND,
    InvalidPasswordException: HTTP_401_UNAUTHORIZED,
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handler(request: Request, exc: AppException) -> None:
        # Если ошибка наследуется от ValueException
        if isinstance(exc, ValueException):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=exc.message)

        # Смотрим на остальные конкретные ошибки
        status: int | None = exceptions_map.get(type(exc))
        if status:
            raise HTTPException(status_code=status, detail=exc.message)

        # Для всех остальных AppException
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message)