"""Mental Wellness model — ментальное здоровье."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class StressLog(Base):
    __tablename__ = "stress_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    level: Mapped[int] = mapped_column(Integer)  # 1-10
    source: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MeditationLog(Base):
    __tablename__ = "meditation_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    technique: Mapped[str | None] = mapped_column(String(50))  # breathing, mindfulness, guided
    notes: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GratitudeEntry(Base):
    __tablename__ = "gratitude_entries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    entry_date: Mapped[datetime] = mapped_column(DateTime)
    item1: Mapped[str] = mapped_column(String(200))
    item2: Mapped[str] = mapped_column(String(200))
    item3: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
