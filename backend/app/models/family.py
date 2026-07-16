"""Family model — семейный режим."""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Family(Base):
    __tablename__ = "families"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    invite_code: Mapped[str] = mapped_column(String(10), unique=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FamilyMember(Base):
    __tablename__ = "family_members"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    family_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("families.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(20), default="member")  # admin, member, child
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SharedTask(Base):
    __tablename__ = "shared_tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    family_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("families.id"))
    title: Mapped[str] = mapped_column(String(500))
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SharedBudget(Base):
    __tablename__ = "shared_budgets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    family_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("families.id"))
    category: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(default=0)
    spent: Mapped[float] = mapped_column(default=0)
    period: Mapped[str] = mapped_column(String(20), default="monthly")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
