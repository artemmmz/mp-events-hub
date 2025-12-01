from fastapi import APIRouter

from modules.auth.delivery.api.http.v1.handlers import router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(router)
