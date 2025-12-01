from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)

from modules.event.domain.aggregate.exceptions import UserRoleNotAllowedException
from seedwork.domain.value_objects.common.exceptions import ValueException
from seedwork.exceptions import AppException
from seedwork.domain.services.exceptions import (
    ExactRoleMismatchException,
    MinRoleTooLowException,
)
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
    ExactRoleMismatchException: HTTP_403_FORBIDDEN,
    MinRoleTooLowException: HTTP_403_FORBIDDEN,
    UserRoleNotAllowedException: HTTP_403_FORBIDDEN,
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