from fastapi import APIRouter

from .v1 import v1_router


auth_router = APIRouter()
auth_router.include_router(v1_router)