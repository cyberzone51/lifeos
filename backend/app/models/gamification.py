"""Gamification model — уровни, достижения, XP."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    level: Mapped[int] = mapped_column(Integer, default=1)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    icon: Mapped[str | None] = mapped_column(String(50))
    xp_reward: Mapped[int] = mapped_column(Integer, default=100)
    requirement_type: Mapped[str] = mapped_column(String(50))  # streak, tasks, finance, etc.
    requirement_value: Mapped[int] = mapped_column(Integer)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    achievement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("achievements.id"))
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DailyChallenge(Base):
    __tablename__ = "daily_challenges"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    challenge_date: Mapped[datetime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(200))
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
