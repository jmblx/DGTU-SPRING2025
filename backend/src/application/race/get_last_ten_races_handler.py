from infrastructure.db.readers.race_reader import RaceReader


class GetLastTenRacesHandler:
    def __init__(self, reader: RaceReader):
        self.reader = reader

    async def handle(self):
        return await self.reader.read_last_10_races()
