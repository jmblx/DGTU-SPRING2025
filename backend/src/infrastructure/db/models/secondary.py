from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models import Base


class RaceResult(Base):
    __tablename__ = "race_result"

    race_id: Mapped[int] = mapped_column(ForeignKey("race.id"), primary_key=True)
    runner_id: Mapped[int] = mapped_column(ForeignKey("runner.id"), primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    finish_time: Mapped[float] = mapped_column(
        Float(precision=5, decimal_return_scale=2),
        nullable=False,
    )

    race = relationship("Race", uselist=False, back_populates="results")
    runner = relationship("Runner", uselist=False, back_populates="race_results")
