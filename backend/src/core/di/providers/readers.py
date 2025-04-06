from dishka import Provider, Scope, provide
from infrastructure.db.readers.race_reader import RaceReader


class ReaderProvider(Provider):
    race_reader = provide(RaceReader, scope=Scope.REQUEST)
