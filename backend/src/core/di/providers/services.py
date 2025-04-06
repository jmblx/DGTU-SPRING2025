from application.calculate_probabilities import ProbabilityCalculatorService
from application.race_chart_generator import RaceChartGenerator
from application.race_simulate import RaceManager
from dishka import Provider, Scope, provide


class ServiceProvider(Provider):
    # calc = provide(Calculate, scope=Scope.REQUEST, provides=Calculate)
    race_manager = provide(RaceManager, scope=Scope.REQUEST, provides=RaceManager)
    probability_calculator_service = provide(
        ProbabilityCalculatorService,
        scope=Scope.REQUEST,
        provides=ProbabilityCalculatorService,
    )
    race_chart_generator = provide(RaceChartGenerator, scope=Scope.REQUEST, provides=RaceChartGenerator)
