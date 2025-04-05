import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_db(
    async_session: AsyncSession,
):
    await async_session.execute(text("SELECT 1"))
