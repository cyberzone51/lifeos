"""Goal model — цели пользователя."""

import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))  # health, finance, education, personal
    target_value: Mapped[float | None] = mapped_column(Numeric(15, 2))
    current_value: Mapped[float | None] = mapped_column(Numeric(15, 2), default=0)
    unit: Mapped[str | None] = mapped_column(String(20))  # kg, km, usd, etc.
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed, paused
    priority: Mapped[int] = mapped_column(Integer, default=2)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GoalMilestone(Base):
    __tablename__ = "goal_milestones"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    goal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("goals.id"))
    title: Mapped[str] = mapped_column(String(200))
    target_value: Mapped[float | None] = mapped_column(Numeric(15, 2))
    is_completed: Mapped[bool] = mapped_column(default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    order: Mapped[int] = mapped_column(Integer, default=0)
