from faststream.rabbit import RabbitRouter

from .email import router as email_router


router = RabbitRouter()

router.include_router(email_router)
