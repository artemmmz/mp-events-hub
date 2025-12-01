from fastapi import APIRouter

from .v1 import v1_router


event_router = APIRouter()
event_router.include_router(v1_router)