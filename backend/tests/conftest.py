import asyncio
import os
import sys
from collections.abc import AsyncGenerator
from typing import Any, TypedDict
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
import docker
from httpx import AsyncClient
from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)

from application.common.interfaces.user_repo import UserRepository
from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.auth_server_token_types import Fingerprint
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientTypeEnum
from domain.entities.role.model import Role
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email, HashedPassword
from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl
from auth_service.tests.config import TEST_DATABASE_URI
from core.di.container import prod_provders
from presentation.web_api.main import create_app

os.environ["USE_NULLPOOL"] = "true"


@pytest.fixture(scope="session")
async def container():
    container = make_async_container(*prod_provders)
    yield container
    await container.close()


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    current_working_directory = os.getcwd()

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../")
    )
    os.chdir(project_root)

    try:
        alembic_cfg = Config(
            os.path.join(os.path.dirname(__file__), "../alembic.ini")
        )
        alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URI)
        command.upgrade(alembic_cfg, "head")
    finally:
        os.chdir(current_working_directory)


@pytest.fixture(scope="session")
async def async_engine(container: AsyncContainer) -> AsyncEngine:
    os.environ["DATABASE_URI"] = TEST_DATABASE_URI
    return create_async_engine(
        url=TEST_DATABASE_URI, echo=True, poolclass=NullPool
    )


@pytest.fixture(scope="session")
async def session_maker(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def async_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[Any, Any]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def real_user_repo(async_session: AsyncSession) -> UserRepository:
    yield UserRepositoryImpl(session=async_session)


@pytest.fixture(scope="session")
async def ac(container) -> AsyncGenerator[AsyncClient, None]:
    app = create_app()
    setup_dishka(container, app)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def teardown_database(async_engine: AsyncEngine):
    """Удаление тестовой базы данных после завершения всех тестов."""
    yield
    async with async_engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))


class StaticEntities(TypedDict):
    roles: list[Role]
    client: Client
    user: User


user_static_data = {
    "id": UUID("e768a26d-8984-4b65-8d3c-f9122cc6245e"),
    "email": "admin@test.com",
    "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$vQVGHMbE2VuwM/Blbd84Qg$HwB3YX/lT153K592RLgGA9gL2Z8Nngc1hxWZ1vcZ1ag",
    "client_id": 1,
}


@pytest.fixture(scope="session")
def static_entities() -> dict:
    """Возвращает данные для создания сущностей."""
    return {
        "client": {
            "name": "Test Client",
            "base_url": "http://test",
            "allowed_redirect_urls": ["http://test"],
            "type": ClientTypeEnum.PUBLIC,
        },
        "roles": [
            {
                "name": "Admin",
                "base_scopes": {"scope1": "1011", "scope2": "1011"},
            },
            {
                "name": "User",
                "base_scopes": {"scope1": "0011", "scope2": "0111"},
            },
        ],
        "user": {
            "id": UUID("e768a26d-8984-4b65-8d3c-f9122cc6245e"),
            "email": "admin@test.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$vQVGHMbE2VuwM/Blbd84Qg$HwB3YX/lT153K592RLgGA9gL2Z8Nngc1hxWZ1vcZ1ag",
        },
    }


@pytest.fixture(scope="session", autouse=True)
async def populate_database(static_entities, session_maker):
    """Наполняет базу данных статическими сущностями перед тестами."""
    async with session_maker() as session:
        client = Client.create(**static_entities["client"])
        session.add(client)
        await session.flush()
        await session.refresh(client)

        roles = [
            Role.create(client_id=client.id.value, **role_data)
            for role_data in static_entities["roles"]
        ]
        session.add_all(roles)
        await session.flush(roles)
        await session.refresh(roles[0])
        await session.refresh(roles[1])

        user = User(
            role_id=roles[0].id,
            **static_entities["user"],
        )
        session.add(user)
        await session.commit()


# --- Фикстуры для сущностей ---
@pytest.fixture
async def admin_role(async_session):
    """Фикстура для получения роли Admin."""
    return await async_session.scalar(
        text("SELECT * FROM roles WHERE name = 'Admin' LIMIT 1")
    )


@pytest.fixture
async def new_user():
    return User.create()


@pytest.fixture
async def user_role_in_db(async_session):
    """Фикстура для получения роли User."""
    return await async_session.scalar(
        text("SELECT * FROM roles WHERE name = 'User' LIMIT 1")
    )


@pytest.fixture
async def client_in_db(async_session):
    """Фикстура для получения клиента."""
    return await async_session.scalar(
        text("SELECT * FROM clients WHERE name = 'Test Client' LIMIT 1")
    )


@pytest.fixture
async def user_in_db(async_session):
    """Фикстура для получения пользователя."""
    return await async_session.get(
        User, UserID(UUID("e768a26d-8984-4b65-8d3c-f9122cc6245e"))
    )


@pytest.fixture(autouse=True)
async def rollback_on_db_mutation(request, async_session):
    """Откатывает изменения базы данных после тестов с меткой `db_mutation`."""
    if "db_mutation" in request.keywords:
        # Начинаем новую транзакцию
        async with async_session.begin_nested():
            yield
            await async_session.rollback()
    else:
        yield


@pytest.fixture
async def auth_headers(mock_user: User, container) -> dict:
    """
    Фикстура для получения заголовков с авторизацией.
    """
    headers = {"Fingerprint": "3ccc784000c0c0c11cab8508dffaa578"}
    http_auth_service = await container.get(HttpAuthServerService)
    access_token, refresh_token = http_auth_service.create_and_save_tokens(
        mock_user, Fingerprint("3ccc784000c0c0c11cab8508dffaa578")
    )

    headers["Authorization"] = f"Bearer {access_token}"
    return headers


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


@pytest.fixture(scope="session")
def nats_container():
    """Запускает NATS в Docker на порту 4222."""
    client = docker.from_env()
    container = client.containers.run(
        "nats:latest",
        ports={"4222/tcp": 4222},
        detach=True,
    )
    yield container
    container.stop()
    container.remove()


@pytest.fixture
async def nats_client(container: AsyncContainer):
    nats_client = await container.get(Client)
    yield nats_client


@pytest.fixture
async def redis_client(container):
    import redis.asyncio as aioredis

    client = await container.get(aioredis.Redis)
    yield client
    await client.flushall()  # Очистить данные после теста
