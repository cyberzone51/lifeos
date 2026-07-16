"""Task model — задачи и планер."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[int] = mapped_column(Integer, default=2)  # 1=low, 2=medium, 3=high
    status: Mapped[str] = mapped_column(String(20), default="pending")
    due_date: Mapped[datetime | None] = mapped_column(DateTime)
    reminder_at: Mapped[datetime | None] = mapped_column(DateTime)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="tasks")
