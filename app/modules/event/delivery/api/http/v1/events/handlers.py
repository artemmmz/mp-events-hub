from datetime import datetime
from uuid import UUID

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
    inject,
)
from fastapi import APIRouter, Depends, UploadFile, Form
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
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
from modules.event.application.use_cases.event.delete import (
    DeleteEventUseCase,
    DeleteEventCommand,
)
from modules.event.application.use_cases.event.unregister_user import (
    UnregisterForEventUseCase,
    UnregisterForEventCommand,
)
from modules.event.application.use_cases.event.update import (
    UpdateEventUseCase,
    UpdateEventCommand,
)
from modules.event.delivery.api.http.v1.events.schemas import (
    CreateEventOutSchema,
    RegisterForEventOutSchema,
    UpdateEventInSchema,
    UpdateEventOutSchema,
)
from modules.event.domain.aggregate.event import Event
from modules.event.domain.aggregate.event_registration import EventRegistration
from seedwork.delivery.api.http.schemas import ErrorSchema
from seedwork.delivery.jwt_utils import get_user_id


register_router = APIRouter(
    prefix="/events",
    tags=["Events", "Register"],
    route_class=DishkaRoute,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"],
    route_class=DishkaRoute,
)
router.include_router(register_router)



@router.post(
    path="/",
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
    use_case: FromDishka[CreateEventUseCase],
    file: UploadFile,
    title: str = Form(...),
    scheduled_at: datetime = Form(...),
    description: str = Form(...),
    city: str | None = Form(None),
    street: str | None = Form(None),
    building_number: int | None = Form(None),
    block: str | None = Form(None),
    auditorium: str | None = Form(None),
    user_id: UUID = Depends(get_user_id),
) -> CreateEventOutSchema:
    command = CreateEventCommand(
        user_id=user_id,
        title=title,
        scheduled_at=scheduled_at,
        description=description,
        city=city,
        street=street,
        building_number=building_number,
        block=block,
        auditorium=auditorium,
        image_fileobject=file,
        image_content_type=file.content_type,
    )

    event: Event = await use_case.act(command)

    return CreateEventOutSchema(event_id=event.id.value)


@router.delete(
    path="/{event_id}",
    response_model=None,
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete event",
    responses={
        HTTP_204_NO_CONTENT: {"model": None, "description": "Delete event"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
)
@inject
async def delete_event(
    event_id: UUID,
    use_case: FromDishka[DeleteEventUseCase],
    user_id: UUID = Depends(get_user_id),
) -> None:
    command = DeleteEventCommand(
        event_id=event_id,
        user_id=user_id,
    )

    await use_case.act(command)


@router.patch(
    path="/{event_id}",
    response_model=UpdateEventOutSchema,
    status_code=HTTP_200_OK,
    summary="Update event",
    responses={
        HTTP_200_OK: {"model": UpdateEventOutSchema, "description": "Update event"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
)
@inject
async def update_event(
    event_id: UUID,
    schema: UpdateEventInSchema,
    use_case: FromDishka[UpdateEventUseCase],
    user_id: UUID = Depends(get_user_id),
) -> UpdateEventOutSchema:
    command = UpdateEventCommand(
        event_id=event_id,
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

    return UpdateEventOutSchema(
        event_id=event.id.value,
    )


@register_router.post(
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


@register_router.delete(
    path="/{event_id}/registrations",
    response_model=None,
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete registration for the event",
    responses={
        HTTP_204_NO_CONTENT: {"model": None, "description": "Delete registration for event"},
        HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid input"},
        HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Unauthorized"},
        HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Resource not found"},
        HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "Conflict rules"},
    }
)
@inject
async def unregister_for_event(
    event_id: UUID,
    use_case: FromDishka[UnregisterForEventUseCase],
    user_id: UUID = Depends(get_user_id),
) -> None:
    command = UnregisterForEventCommand(
        event_id=event_id,
        user_id=user_id,
    )

    await use_case.act(command)