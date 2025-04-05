from application.common.interfaces.uow import Uow
from dishka import Provider, Scope, provide
from infrastructure.db.uow import SAUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession


class UowProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Uow)
    async def provide_session(self, session: AsyncSession) -> SAUnitOfWork:
        return SAUnitOfWork(session)
