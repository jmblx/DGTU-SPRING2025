from dishka import Provider, Scope, provide

from application.race_simulate import RaceManager


class ServiceProvider(Provider):
    # calc = provide(Calculate, scope=Scope.REQUEST, provides=Calculate)
    race_manager = provide(RaceManager, scope=Scope.REQUEST, provides=RaceManager)
