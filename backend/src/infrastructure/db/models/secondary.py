from decimal import Decimal

from infrastructure.db.models import Base
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RaceResult(Base):
    __tablename__ = "race_result"

    race_id: Mapped[int] = mapped_column(ForeignKey("race.id"), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    finish_time: Mapped[Decimal] = mapped_column(Numeric(5, 2))

    race = relationship("Race", uselist=False, back_populates="results")
    student = relationship("Student", uselist=False, back_populates="race_results")
