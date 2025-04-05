from dataclasses import dataclass

from application.common.errors.base import ApplicationError


@dataclass(eq=False)
class RunnerParameterValidationError(ApplicationError):
    details: str

    @property
    def title(self) -> str:
        return "Invalid runner parameters. Details: %s" % self.details


@dataclass(eq=False)
class RunnerNotFoundByID(ApplicationError):
    @property
    def title(self) -> str:
        return "Runner not found"
