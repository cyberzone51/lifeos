"""Finance API — эндпоинты для финансов с интеграцией БД."""

import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.finance_service import FinanceService
from app.repositories.finance_repo import FinanceRepository

router = APIRouter(prefix="/finance", tags=["Finance"])


class ExpenseCreate(BaseModel):
    amount: float
    currency_code: str = "USD"
    category_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class ExpenseResponse(BaseModel):
    id: str
    amount: float
    currency_code: str
    category_id: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    expense_date: datetime
    created_at: datetime


class IncomeCreate(BaseModel):
    amount: float
    currency_code: str = "USD"
    category_name: Optional[str] = None
    description: Optional[str] = None


class StatisticsResponse(BaseModel):
    period: str
    total_expenses: float
    total_income: float
    balance: float
    by_category: List[dict]


@router.post("/expenses", response_model=ExpenseResponse)
async def create_expense(
    request: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать расход."""
    user_id = uuid.uuid4()  # Заглушка для тестирования
    
    finance_service = FinanceService(db)
    expense = await finance_service.create_expense(
        user_id=user_id,
        amount=request.amount,
        currency_code=request.currency_code,
        category_name=request.category_name or "other",
        description=request.description,
        tags=request.tags,
    )

    return ExpenseResponse(
        id=str(expense.id),
        amount=float(expense.amount),
        currency_code=expense.currency_code,
        category_id=str(expense.category_id) if expense.category_id else None,
        description=expense.description,
        tags=expense.tags,
        expense_date=expense.expense_date,
        created_at=expense.created_at,
    )


@router.get("/expenses", response_model=List[ExpenseResponse])
async def list_expenses(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Получить список расходов."""
    user_id = uuid.uuid4()  # Заглушка
    
    finance_repo = FinanceRepository(db)
    expenses = await finance_repo.get_expenses(
        user_id, start_date, end_date, limit
    )

    return [
        ExpenseResponse(
            id=str(e.id),
            amount=float(e.amount),
            currency_code=e.currency_code,
            category_id=str(e.category_id) if e.category_id else None,
            description=e.description,
            tags=e.tags,
            expense_date=e.expense_date,
            created_at=e.created_at,
        )
        for e in expenses
    ]


@router.post("/incomes")
async def create_income(
    request: IncomeCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать доход."""
    user_id = uuid.uuid4()  # Заглушка
    
    finance_service = FinanceService(db)
    income = await finance_service.create_income(
        user_id=user_id,
        amount=request.amount,
        currency_code=request.currency_code,
        category_name=request.category_name or "other",
        description=request.description,
    )

    return {
        "status": "created",
        "id": str(income.id),
    }


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    db: AsyncSession = Depends(get_db),
):
    """Получить статистику за текущий месяц."""
    user_id = uuid.uuid4()  # Заглушка
    
    finance_service = FinanceService(db)
    summary = await finance_service.get_monthly_summary(user_id)

    return StatisticsResponse(
        period=summary["period"],
        total_expenses=summary["total_expenses"],
        total_income=summary["total_income"],
        balance=summary["balance"],
        by_category=summary["by_category"],
    )


@router.get("/recent")
async def get_recent_expenses(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Получить последние расходы."""
    user_id = uuid.uuid4()  # Заглушка
    
    finance_service = FinanceService(db)
    return await finance_service.get_recent_expenses(user_id, limit)
