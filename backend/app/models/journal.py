"""Journal model — дневник."""

import uuid
from datetime import datetime, date
from sqlalchemy import String, Integer, Text, Date, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text)
    mood: Mapped[int | None] = mapped_column(Integer)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    entry_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
