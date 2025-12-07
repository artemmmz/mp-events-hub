from datetime import datetime, timezone

import pytest
from asyncpg.pgproto.pgproto import timedelta
from dishka import AsyncContainer
from httpx import AsyncClient, Response
from starlette.status import (
    HTTP_201_CREATED,
)

from modules.event.delivery.api.http.v1.events.schemas import (
    CreateEventInSchema,
    CreateEventOutSchema,
)
from modules.event.infra.dm.event import IEventDm
from modules.event.infra.pg.models import EventOrm
from tests.message_templates import build_status_message


@pytest.mark.integration
async def test_organizer_without_location(
    organizer_access_token: str,
    client: AsyncClient,
    ioc_container: AsyncContainer,
) -> None:
    payload = CreateEventInSchema(
        title="ру хайперпоп 2021 фест",
        scheduled_at=datetime.now(tz=timezone.utc) + timedelta(days=2),
        description="слушаем прайм музыку, вспоминаем о школе, прийдет парадокси кста",
    )

    response: Response = await client.post(
        url="/api/v1/events",
        content=payload.model_dump_json(),
        headers={
            "Authorization": f"Bearer {organizer_access_token}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == HTTP_201_CREATED, build_status_message(
        actual_status=response.status_code,
        expected_status=HTTP_201_CREATED,
        details=response.text,
    )

    response_schema = CreateEventOutSchema.model_validate_json(
        json_data=response.text
    )

    async with ioc_container() as cont:
        event_dm: IEventDm = await cont.get(IEventDm)

        event_orm: EventOrm | None = await (
            event_dm.find_by_id(_id=response_schema.event_id)
        )

        assert event_orm is not None, "Expected event to exist in the database, but got None"


@pytest.mark.integration
async def test_organizer_with_location(
    organizer_access_token: str,
    client: AsyncClient,
    ioc_container: AsyncContainer,
) -> None:
    payload = CreateEventInSchema(
        title="ру хайперпоп 2021 фест",
        scheduled_at=datetime.now(tz=timezone.utc) + + timedelta(days=2),
        description="слушаем прайм музыку, вспоминаем о школе, прийдет парадокси кста",
        city="Moscow",
        street="Nyyaa",
        building_number=11,
        block="102a",
        auditorium="221",
    )

    response: Response = await client.post(
        url="/api/v1/events",
        content=payload.model_dump_json(),
        headers={
            "Authorization": f"Bearer {organizer_access_token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == HTTP_201_CREATED, build_status_message(
        actual_status=response.status_code,
        expected_status=HTTP_201_CREATED,
        details=response.text,
    )

    response_schema = CreateEventOutSchema.model_validate_json(
        json_data=response.text,
    )

    async with ioc_container() as cont:
        event_dm: IEventDm = await cont.get(IEventDm)

        event_orm: EventOrm | None = await (
            event_dm.find_by_id(_id=response_schema.event_id)
        )

        assert event_orm is not None, "Expected event to exist in the database, but got None"
        assert event_orm.address is not None, "Event address orm was not saved"
        assert event_orm.address.building is not None, "Event building orm was not saved"
