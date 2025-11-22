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
)

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
        if exceptions_map.get(type(exc), None):
            status: int | None = exceptions_map.get(type(exc))
            raise HTTPException(status_code=status, detail=exc.message)
