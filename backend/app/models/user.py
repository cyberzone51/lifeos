"""User model — основная сущность пользователя."""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, unique=True, nullable=True
    )
    username: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(20))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    premium_expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    language_code: Mapped[str] = mapped_column(String(10), default="en")
    currency_code: Mapped[str] = mapped_column(String(3), default="USD")
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="user")
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    habits: Mapped[list["Habit"]] = relationship(back_populates="user")
    ai_conversations: Mapped[list["AIConversation"]] = relationship(
        back_populates="user"
    )
    ai_memories: Mapped[list["AIMemory"]] = relationship(back_populates="user")
