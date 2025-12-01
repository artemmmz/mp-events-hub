import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from fastapi import FastAPI
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from bootstrap.ioc import get_container
from modules.email.delivery.api import email_router
from modules.event.delivery.api.events import event_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()

    async with container() as cont:
        faststream: FastStream = await cont.get(FastStream)
        broker: RabbitBroker = await cont.get(RabbitBroker)
        broker.include_router(email_router)
        broker.include_router(event_router)

        task = asyncio.create_task(faststream.run())

        yield

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        await app.state.dishka_container.close()