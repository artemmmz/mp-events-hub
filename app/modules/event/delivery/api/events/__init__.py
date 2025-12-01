from faststream.rabbit import RabbitRouter

from .auth import router as auth_router


event_router = RabbitRouter()
event_router.include_router(auth_router)