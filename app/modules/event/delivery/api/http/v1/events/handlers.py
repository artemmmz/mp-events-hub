from uuid import UUID

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    inject,
)
from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from modules.event.application.use_cases.event.create import (
    CreateEventUseCase,
    CreateEventCommand,
)
from modules.event.application.use_cases.event.register_user import (
    RegisterForEventUseCase,
    RegisterForEventCommand,
)
from modules.event.delivery.api.http.v1.events.schemas import (
    CreateEventInSchema,
    CreateEventOutSchema,
    RegisterForEventOutSchema,
)
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.event_registration import EventRegistration
from seedwork.delivery.api.http.schemas import ErrorSchema
from seedwork.delivery.jwt_utils import get_user_id

router = APIRouter(
    prefix="/events",
    route_class=DishkaRoute,
)


@router.post(
    path="/create",
    response_model=CreateEventOutSchema,
    status_code=HTTP_201_CREATED,
    summary="Create a new event",
    responses={
        HTTP_201_CREATED: {"model": CreateEventOutSchema, "description": "Create event"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
)
@inject
async def create_event(
    schema: CreateEventInSchema,
    use_case: FromDishka[CreateEventUseCase],
    user_id: UUID = Depends(get_user_id),
) -> CreateEventOutSchema:
    command = CreateEventCommand(
        user_id=user_id,
        title=schema.title,
        scheduled_at=schema.scheduled_at,
        description=schema.description,
        city=schema.city,
        street=schema.street,
        building_number=schema.building_number,
        block=schema.block,
        auditorium=schema.auditorium,
    )

    event: Event = await use_case.act(command)

    return CreateEventOutSchema(event_id=event.id.value)


@router.post(
    path="/{event_id}/registrations",
    response_model=RegisterForEventOutSchema,
    status_code=HTTP_201_CREATED,
    summary="Registration for the event",
    responses={
        HTTP_201_CREATED: {"model": RegisterForEventOutSchema, "description": "Register for event"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
)
@inject
async def register_for_event(
    event_id: UUID,
    use_case: FromDishka[RegisterForEventUseCase],
    user_id: UUID = Depends(get_user_id),
) -> RegisterForEventOutSchema:
    command = RegisterForEventCommand(
        user_id=user_id,
        event_id=event_id,
    )

    event_registration: EventRegistration = await use_case.act(command)

    return RegisterForEventOutSchema(
        user_id=event_registration.user_id.value,
        event_id=event_registration.event_id.value
    )