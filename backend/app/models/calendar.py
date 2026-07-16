"""Calendar model — календарь и события."""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(500))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime | None] = mapped_column(DateTime)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence: Mapped[str | None] = mapped_column(String(20))  # daily, weekly, monthly, yearly
    color: Mapped[str | None] = mapped_column(String(7))
    reminder_minutes: Mapped[int | None] = mapped_column(default=15)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
