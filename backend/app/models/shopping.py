"""Shopping model — умные покупки."""

import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(200))
    budget: Mapped[float | None] = mapped_column(Numeric(10, 2))
    currency_code: Mapped[str] = mapped_column(String(3), default="USD")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shopping_lists.id"))
    name: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    estimated_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    actual_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    is_purchased: Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
