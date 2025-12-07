import os
import sys

import pika
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis

from tests.ioc.container import get_test_container

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from collections.abc import AsyncGenerator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import AsyncRedisContainer
from testcontainers.rabbitmq import RabbitMqContainer

from app.bootstrap.main import create_app


@pytest.fixture(scope="session")
async def redis_client() -> AsyncGenerator[Redis]:
    with AsyncRedisContainer() as redis_cont:
        redis: Redis = await redis_cont.get_async_client()
        yield redis


@pytest.fixture(scope="session")
async def rmq_url() -> AsyncGenerator[str]:
    with RabbitMqContainer() as rmq:
        params = rmq.get_connection_params()
        rmq_url: str = _to_connection_string(params=params)
        print(f"rmq url: {rmq_url}")
        yield rmq_url


@pytest.fixture(scope="session")
async def postgres_url() -> AsyncGenerator[str]:
    postgres = PostgresContainer("postgres:18-alpine")

    if os.name == "nt":  # workaround для Windows
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        print(f"postgres_url: {postgres_url_}")
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    alembic_ini_path = os.path.join(base_dir, "app/alembic.ini")

    alembic_cfg = AlembicConfig(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def _upgrade_schema_db(alembic_config: AlembicConfig) -> None:
    upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
async def ioc_container(
    postgres_url: str,
    rmq_url: str,
    redis_client: Redis,
) -> AsyncContainer:
    test_container: AsyncContainer = await get_test_container(
        connection_string=postgres_url,
        rmq_url=rmq_url,
        redis=redis_client,
    )

    return test_container


@pytest.fixture(scope="session")
async def app(
    ioc_container: AsyncContainer,
) -> AsyncGenerator[FastAPI]:
    app = create_app()
    setup_dishka(ioc_container, app)



    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield client


def _to_connection_string(params: pika.ConnectionParameters) -> str:
    creds = params.credentials
    username = creds.username if creds else "guest"
    password = creds.password if creds else "guest"

    vhost = params.virtual_host or "/"
    if vhost == "/":
        vhost = "%2f"

    return f"amqp://{username}:{password}@{params.host}:{params.port}/{vhost}"