import os
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.db.config import DatabaseConfig


class DBProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_engine(self, config: DatabaseConfig) -> AsyncEngine:
        pool_class = (
            NullPool
            if os.getenv("USE_NULLPOOL", "false").lower() == "true"
            else None
        )
        return create_async_engine(config.db_uri, poolclass=pool_class)

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
