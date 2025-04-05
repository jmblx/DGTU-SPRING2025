from decimal import Decimal

from infrastructure.db.models import Base
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    colour: Mapped[str] = mapped_column(String(20))
    reaction_time: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        nullable=False,
    )
    acceleration: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
    )
    max_speed: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
    )
    speed_decay: Mapped[Decimal] = mapped_column(
        Numeric(4, 3),
        nullable=False,
    )

    race_results = relationship("RaceResult", uselist=True, back_populates="student")

    def __repr__(self):
        return f"<Student {self.colour}-{self.id}>"
