from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from infrastructure.db.models import Base


class Student(Base):
    __tablename__ = 'student'

    colour: Mapped[str] = mapped_column(String(20), primary_key=True)
    
