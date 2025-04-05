import logging
from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class RaceData(TypedDict):


class RaceReader:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_last_10_races(self):

