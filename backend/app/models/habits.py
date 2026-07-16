"""Habit models — привычки и история."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    icon: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(7))
    frequency: Mapped[str] = mapped_column(String(20), default="daily")
    target_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="habits")
    logs: Mapped[list["HabitLog"]] = relationship(back_populates="habit")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    habit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("habits.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    completed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    value: Mapped[float | None] = mapped_column(Numeric(10, 2))
    notes: Mapped[str | None] = mapped_column(Text)

    habit: Mapped["Habit"] = relationship(back_populates="logs")
