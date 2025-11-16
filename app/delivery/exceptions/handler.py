from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from seedwork.exceptions import AppException

exceptions_map: dict[type[AppException], int] = {
    AppException: HTTP_500_INTERNAL_SERVER_ERROR,
}

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handler(request: Request, exc: AppException) -> None:
        if exceptions_map.get(type(exc), None):
            status: int | None = exceptions_map.get(type(exc))
            raise HTTPException(status_code=status, detail=exc.message)
