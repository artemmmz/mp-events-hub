from faststream.rabbit import RabbitRouter

from bootstrap.ioc import get_container
from modules.auth.domain.events import RegistrationRequestedUserEvent
from modules.email.application.send_confirm_code import (
    SendConfirmCodeUseCase,
    SendConfirmCodeCommand,
)
from modules.email.infra.rmq.queues import REGISTRATION_REQUESTED_USER_EVENT_QUEUE


router = RabbitRouter()


@router.subscriber(
    queue=REGISTRATION_REQUESTED_USER_EVENT_QUEUE,
)
async def send_verification_code(
    event: RegistrationRequestedUserEvent,
) -> None:
    container = get_container()

    async with container() as cont:
        use_case: SendConfirmCodeUseCase = await cont.get(SendConfirmCodeUseCase)

        command = SendConfirmCodeCommand(
            email=event.email,
            confirm_code=event.confirm_code,
            subject="Код подтверждения, Московский Политех"
        )

        await use_case.act(command=command)