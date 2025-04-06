from infrastructure.db.readers.race_reader import RacePositions, RaceReader


class GetLastTenRacesHandler:
    def __init__(self, reader: RaceReader):
        self.reader = reader

    async def handle(self, last_race_id: int) -> dict[int, RacePositions]:
        """Преобразует TypedDict в Pydantic модель"""
        raw_data = await self.reader.read_last_10_races(last_race_id)
        return raw_data
