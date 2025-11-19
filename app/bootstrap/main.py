from fastapi import FastAPI
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka

from bootstrap.ioc import get_container
from bootstrap.lifespan import lifespan
from delivery.api import v1_router
from delivery.exceptions.handler import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        debug=False,
        lifespan=lifespan,
        title="My school events",
        summary="",
        docs_url="/docs",
        root_path="/api",
    )
    app.include_router(v1_router)
    register_exception_handlers(app=app)

    return app


def main() -> FastAPI:
    app: FastAPI = create_app()

    container: AsyncContainer = get_container()
    setup_dishka(container=container, app=app)

    return app