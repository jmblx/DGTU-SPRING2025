from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.interfaces.uow import Uow
from infrastructure.db.uow import SAUnitOfWork


class UowProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Uow)
    async def provide_session(self, session: AsyncSession) -> SAUnitOfWork:
        return SAUnitOfWork(session)
