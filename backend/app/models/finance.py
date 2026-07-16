"""Finance models — расходы, доходы, бюджеты."""

import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(200))
    icon: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(7))
    is_system: Mapped[bool] = mapped_column(default=False)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("expense_categories.id")
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    currency_code: Mapped[str] = mapped_column(String(3))
    description: Mapped[str | None] = mapped_column(Text)
    receipt_url: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    expense_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="expenses")
    category: Mapped["ExpenseCategory"] = relationship(back_populates="expenses")


class IncomeCategory(Base):
    __tablename__ = "income_categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(200))
    icon: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(7))
    is_system: Mapped[bool] = mapped_column(default=False)

    incomes: Mapped[list["Income"]] = relationship(back_populates="category")


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("income_categories.id")
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    currency_code: Mapped[str] = mapped_column(String(3))
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    income_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="incomes")
    category: Mapped["IncomeCategory"] = relationship(back_populates="incomes")


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("expense_categories.id")
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    period: Mapped[str] = mapped_column(String(20))  # weekly, monthly, yearly
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
