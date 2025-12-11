from faststream.rabbit import RabbitRouter

from bootstrap.ioc import get_container
from seedwork.domain.events.auth import (
    RequestedRegistrationUserEvent,
    RequestResetPasswordEvent,
)
from modules.email.application.send_confirm_code import (
    SendConfirmCodeUseCase,
    SendConfirmCodeCommand,
)
from seedwork.infra.rmq.queues import (
    REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
    REQUESTED_RESET_PASSWORD_USER_EVENT_QUEUE,
)


router = RabbitRouter()


@router.subscriber(
    queue=REQUESTED_REGISTRATION_USER_EVENT_QUEUE,
)
async def requested_registration_user(
    event: RequestedRegistrationUserEvent,
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


@router.subscriber(
    queue=REQUESTED_RESET_PASSWORD_USER_EVENT_QUEUE,
)
async def requested_reset_password(
    event: RequestResetPasswordEvent,
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