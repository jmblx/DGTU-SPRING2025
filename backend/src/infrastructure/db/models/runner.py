from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models import Base


class Runner(Base):
    __tablename__ = "runner"

    id: Mapped[int] = mapped_column(primary_key=True)
    colour: Mapped[str] = mapped_column(String(20))

    reaction_time: Mapped[float] = mapped_column(
        Float(precision=3, decimal_return_scale=2),
        nullable=False,
    )
    acceleration: Mapped[float] = mapped_column(
        Float(precision=4, decimal_return_scale=2),
        nullable=False,
    )
    max_speed: Mapped[float] = mapped_column(
        Float(precision=4, decimal_return_scale=2),
        nullable=False,
    )
    speed_decay: Mapped[float] = mapped_column(
        Float(precision=4, decimal_return_scale=3),
        nullable=False,
    )

    race_results = relationship("RaceResult", uselist=True, back_populates="runner")

    def __repr__(self):
        return f"<Runner {self.colour}-{self.id}>"
