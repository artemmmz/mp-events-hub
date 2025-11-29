from fastapi import APIRouter

from delivery.api.http.v1.auth import auth_router


v1_router = APIRouter()
v1_router.include_router(auth_router)
