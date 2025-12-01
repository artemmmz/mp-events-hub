from faststream.rabbit import RabbitRouter

from bootstrap.ioc import get_container
from modules.event.application.use_cases.auth.confirm import (
    ConfirmRegisterUseCase,
    ConfirmRegisterCommand,
)
from seedwork.domain.events.auth import ConfirmRegistrationUserEvent
from seedwork.infra.rmq.queues import CONFIRM_REGISTRATION_USER_EVENT_QUEUE


router = RabbitRouter()


@router.subscriber(
    queue=CONFIRM_REGISTRATION_USER_EVENT_QUEUE,
)
async def confirm_registration_user(
    event: ConfirmRegistrationUserEvent,
) -> None:
    """Event driven replication of the user’s role"""

    container = get_container()

    async with container() as cont:
        use_case: ConfirmRegisterUseCase = await cont.get(ConfirmRegisterUseCase)
        command = ConfirmRegisterCommand(
            user_id=event.user_id,
            role=event.role,
        )

        await use_case.act(command)