"""Schemas package — Pydantic модели для API."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Common
class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int


# AI
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    intent: dict
    action_taken: Optional[dict] = None


# Finance
class ExpenseCreate(BaseModel):
    amount: float
    currency_code: str = "USD"
    category_id: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    expense_date: Optional[datetime] = None


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
    category_id: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    income_date: Optional[datetime] = None


# Tasks
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 2
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: int
    status: str
    due_date: Optional[datetime]
    reminder_at: Optional[datetime]
    tags: Optional[List[str]]
    created_at: datetime


# Auth
class TelegramLoginRequest(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
