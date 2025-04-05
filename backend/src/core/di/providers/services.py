from dishka import Provider, Scope, provide

from application.race_simulate import RaceBroadcaster, RaceManager


class ServiceProvider(Provider):
    # calc = provide(Calculate, scope=Scope.REQUEST, provides=Calculate)
    broadcaster_manager = provide(
        RaceBroadcaster, scope=Scope.SESSION, provides=RaceBroadcaster
    )
    race_manager = provide(RaceManager, scope=Scope.REQUEST, provides=RaceManager)
