"""Health models — вес, сон, настроение."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class WeightLog(Base):
    __tablename__ = "weight_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    weight: Mapped[float] = mapped_column(Numeric(5, 2))
    unit: Mapped[str] = mapped_column(String(5), default="kg")
    logged_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    bedtime: Mapped[datetime] = mapped_column(DateTime)
    wake_time: Mapped[datetime] = mapped_column(DateTime)
    quality: Mapped[int | None] = mapped_column(Integer)  # 1-5
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class MoodLog(Base):
    __tablename__ = "mood_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    mood: Mapped[int] = mapped_column(Integer)  # 1-10
    notes: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
