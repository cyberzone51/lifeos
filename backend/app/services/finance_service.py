"""Finance Service — бизнес-логика финансов."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.finance import Expense, Income
from app.repositories.finance_repo import FinanceRepository


class FinanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = FinanceRepository(db)

    async def create_expense(
        self,
        user_id: uuid.UUID,
        amount: float,
        currency_code: str,
        category_name: str,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> Expense:
        """Создание расхода с автоматической категоризацией."""
        category = await self.repo.get_or_create_category(user_id, category_name)
        
        expense = await self.repo.create_expense(
            user_id=user_id,
            amount=amount,
            currency_code=currency_code,
            category_id=category.id,
            description=description,
            tags=tags,
            expense_date=datetime.utcnow(),
        )
        return expense

    async def create_income(
        self,
        user_id: uuid.UUID,
        amount: float,
        currency_code: str,
        category_name: str,
        description: str | None = None,
    ) -> Income:
        """Создание дохода."""
        from app.models.finance import IncomeCategory
        
        # Get or create income category
        from sqlalchemy import select, and_
        query = select(IncomeCategory).where(
            and_(
                IncomeCategory.user_id == user_id,
                IncomeCategory.name == category_name,
            )
        )
        result = await self.db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            category = IncomeCategory(user_id=user_id, name=category_name)
            self.db.add(category)
            await self.db.flush()
        
        income = await self.repo.create_income(
            user_id=user_id,
            amount=amount,
            currency_code=currency_code,
            category_id=category.id,
            description=description,
            income_date=datetime.utcnow(),
        )
        return income

    async def get_monthly_summary(self, user_id: uuid.UUID) -> dict:
        """Получение сводки за текущий месяц."""
        now = datetime.utcnow()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        total_expenses = await self.repo.get_expenses_total(
            user_id, start_of_month, end_of_month
        )
        total_income = await self.repo.get_incomes_total(
            user_id, start_of_month, end_of_month
        )
        by_category = await self.repo.get_expenses_by_category(
            user_id, start_of_month, end_of_month
        )

        return {
            "period": f"{start_of_month.strftime('%Y-%m')}",
            "total_expenses": float(total_expenses),
            "total_income": float(total_income),
            "balance": float(total_income) - float(total_expenses),
            "by_category": by_category,
        }

    async def get_recent_expenses(
        self, user_id: uuid.UUID, limit: int = 10
    ) -> list[dict]:
        """Получение последних расходов."""
        expenses = await self.repo.get_expenses(user_id, limit=limit)
        return [
            {
                "id": str(e.id),
                "amount": float(e.amount),
                "currency": e.currency_code,
                "description": e.description,
                "date": e.expense_date.isoformat(),
            }
            for e in expenses
        ]
