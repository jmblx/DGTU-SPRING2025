from datetime import datetime

from infrastructure.db.models import Base
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Race(Base):
    __tablename__ = "race"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    results = relationship("RaceResult", uselist=True, back_populates="race")
