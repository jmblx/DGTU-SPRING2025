import os
import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import docker
import pytest
from alembic import command
from alembic.config import Config
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.tests.config import TEST_DATABASE_URI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from core.di.container import prod_provders
from presentation.web_api.main import create_app

os.environ["USE_NULLPOOL"] = "true"


@pytest.fixture(scope="session")
async def container():
    container = make_async_container(*prod_provders)
    yield container
    await container.close()


@pytest.fixture(scope="session", autouse=True)
def _apply_migrations() -> None:
    current_working_directory = Path.cwd()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    os.chdir(project_root)

    try:
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
        alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URI)
        os.environ["TESTING"] = "true"
        command.upgrade(alembic_cfg, "head")
    finally:
        os.chdir(current_working_directory)


@pytest.fixture(scope="session")
async def async_engine(container: AsyncContainer) -> AsyncEngine:
    os.environ["DATABASE_URI"] = TEST_DATABASE_URI
    return create_async_engine(url=TEST_DATABASE_URI, echo=True, poolclass=NullPool)


@pytest.fixture(scope="session")
async def session_maker(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine, expire_on_commit=False)


@pytest.fixture
async def async_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[Any, Any]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def ac(container) -> AsyncGenerator[AsyncClient, None]:
    app = create_app()
    setup_dishka(container, app)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def _teardown_database(async_engine: AsyncEngine):
    """Удаление тестовой базы данных после завершения всех тестов."""
    yield
    async with async_engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))


@pytest.fixture(scope="session")
def redis_container():
    """Запускает Redis в Docker на порту 6379."""
    client = docker.from_env()
    container = client.containers.run(
        "redis:latest",
        ports={"6379/tcp": 6379},
        detach=True,
    )
    yield container
    container.stop()
    container.remove()


@pytest.fixture
async def redis_client(container):
    import redis.asyncio as aioredis

    client = await container.get(aioredis.Redis)
    yield client
    await client.flushall()
