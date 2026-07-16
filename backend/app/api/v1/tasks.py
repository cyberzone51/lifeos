"""Tasks API — эндпоинты для задач."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 2  # 1=low, 2=medium, 3=high
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


@router.post("/", response_model=TaskResponse)
async def create_task(request: TaskCreate):
    """Создать задачу."""
    return TaskResponse(
        id="mock-id",
        title=request.title,
        description=request.description,
        priority=request.priority,
        status="pending",
        due_date=request.due_date,
        reminder_at=request.reminder_at,
        tags=request.tags,
        created_at=datetime.utcnow(),
    )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
):
    """Получить список задач."""
    return []


@router.patch("/{task_id}")
async def update_task(task_id: str):
    """Обновить задачу."""
    return {"status": "updated"}


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Удалить задачу."""
    return {"status": "deleted"}
