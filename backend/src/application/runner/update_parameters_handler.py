from dataclasses import dataclass

from application.common.interfaces.uow import Uow
from application.runner.common.errors import (
    RunnerNotFoundByID,
    RunnerParameterValidationError,
)
from infrastructure.db.models import Runner
from infrastructure.db.repositories.runner_repo import RunnerRepo


@dataclass
class UpdateRunnerParametersCommand:
    runner_id: int
    reaction_time: float | None
    acceleration: float | None
    max_speed: float | None
    speed_decay: float | None


class UpdateRunnerParametersHandler:
    def __init__(self, runner_repo: RunnerRepo, uow: Uow):
        self.runner_repo = runner_repo
        self.uow = uow

    async def handle(self, command: UpdateRunnerParametersCommand) -> None:
        runner = await self.runner_repo.get_runner(command.runner_id)
        if runner is None:
            raise RunnerNotFoundByID

        if all(
            getattr(command, field) in (None, 0)
            for field in ["reaction_time", "acceleration", "max_speed", "speed_decay"]
        ):
            raise RunnerParameterValidationError("No parameters provided for update.")

        if command.reaction_time not in (None, 0) and not (0.1 <= command.reaction_time <= 0.3):
            raise RunnerParameterValidationError(
                f"Invalid reaction_time: {command.reaction_time}. Must be between 0.1 and 0.3 seconds."
            )

        if command.acceleration not in (None, 0) and not (2 <= command.acceleration <= 10):
            raise RunnerParameterValidationError(
                f"Invalid acceleration: {command.acceleration}. Must be between 2 and 10 m/s^2."
            )

        if command.max_speed not in (None, 0) and not (7 <= command.max_speed <= 12):
            raise RunnerParameterValidationError(
                f"Invalid max_speed: {command.max_speed}. Must be between 7 and 12 m/s."
            )

        if command.speed_decay not in (None, 0) and not (0.05 <= command.speed_decay <= 0.5):
            raise RunnerParameterValidationError(
                f"Invalid speed_decay: {command.speed_decay}. Must be between 0.05 and 0.5."
            )

        for key, value in command.__dict__.items():
            if key != "runner_id" and value not in (None, 0):
                setattr(runner, key, value)

        await self.uow.commit()
