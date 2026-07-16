"""Finance Repository — работа с финансами."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.finance import Expense, Income, ExpenseCategory


class FinanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Expenses
    async def create_expense(self, user_id: uuid.UUID, **kwargs) -> Expense:
        expense = Expense(user_id=user_id, **kwargs)
        self.db.add(expense)
        await self.db.flush()
        return expense

    async def get_expenses(
        self,
        user_id: uuid.UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
    ) -> list[Expense]:
        query = select(Expense).where(Expense.user_id == user_id)
        
        if start_date:
            query = query.where(Expense.expense_date >= start_date)
        if end_date:
            query = query.where(Expense.expense_date <= end_date)
            
        query = query.order_by(Expense.expense_date.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_expenses_total(
        self,
        user_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        query = select(func.sum(Expense.amount)).where(
            and_(
                Expense.user_id == user_id,
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date,
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0.0

    async def get_expenses_by_category(
        self,
        user_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict]:
        query = (
            select(
                Expense.category_id,
                func.sum(Expense.amount).label("total"),
                func.count(Expense.id).label("count"),
            )
            .where(
                and_(
                    Expense.user_id == user_id,
                    Expense.expense_date >= start_date,
                    Expense.expense_date <= end_date,
                )
            )
            .group_by(Expense.category_id)
        )
        result = await self.db.execute(query)
        return [
            {"category_id": row[0], "total": float(row[1]), "count": row[2]}
            for row in result.all()
        ]

    # Categories
    async def get_or_create_category(
        self, user_id: uuid.UUID, name: str
    ) -> ExpenseCategory:
        query = select(ExpenseCategory).where(
            and_(
                ExpenseCategory.user_id == user_id,
                ExpenseCategory.name == name,
            )
        )
        result = await self.db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            category = ExpenseCategory(user_id=user_id, name=name)
            self.db.add(category)
            await self.db.flush()
        
        return category

    # Incomes
    async def create_income(self, user_id: uuid.UUID, **kwargs) -> Income:
        income = Income(user_id=user_id, **kwargs)
        self.db.add(income)
        await self.db.flush()
        return income

    async def get_incomes_total(
        self,
        user_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        query = select(func.sum(Income.amount)).where(
            and_(
                Income.user_id == user_id,
                Income.income_date >= start_date,
                Income.income_date <= end_date,
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0.0
