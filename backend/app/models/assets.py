"""Asset model — учет имущества."""

import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50))  # car, home, electronics, other
    purchase_date: Mapped[datetime | None] = mapped_column(DateTime)
    purchase_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    current_value: Mapped[float | None] = mapped_column(Numeric(12, 2))
    currency_code: Mapped[str] = mapped_column(String(3), default="USD")
    serial_number: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)
    photo_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AssetReminder(Base):
    __tablename__ = "asset_reminders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    reminder_type: Mapped[str] = mapped_column(String(50))  # insurance, maintenance, payment
    next_date: Mapped[datetime] = mapped_column(DateTime)
    repeat_days: Mapped[int | None] = mapped_column(default=365)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
