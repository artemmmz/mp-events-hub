from faststream.rabbit import RabbitRouter

from .events.handler import router


email_router = RabbitRouter()
email_router.include_router(router)