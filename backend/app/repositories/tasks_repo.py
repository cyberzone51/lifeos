"""Tasks Repository — работа с задачами."""

import uuid
from datetime import datetime
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task


class TasksRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, **kwargs) -> Task:
        task = Task(user_id=user_id, **kwargs)
        self.db.add(task)
        await self.db.flush()
        return task

    async def get_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task | None:
        query = select(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_tasks(
        self,
        user_id: uuid.UUID,
        status: str | None = None,
        due_before: datetime | None = None,
        limit: int = 50,
    ) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id)
        
        if status:
            query = query.where(Task.status == status)
        if due_before:
            query = query.where(Task.due_date <= due_before)
            
        query = query.order_by(Task.due_date.asc().nullslast()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, task_id: uuid.UUID, user_id: uuid.UUID, **kwargs) -> Task | None:
        task = await self.get_by_id(task_id, user_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            await self.db.flush()
        return task

    async def complete(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task | None:
        return await self.update(task_id, user_id, status="completed")

    async def delete(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        query = delete(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.rowcount > 0

    async def get_today_tasks(self, user_id: uuid.UUID) -> list[Task]:
        today = datetime.utcnow().replace(hour=23, minute=59, second=59)
        return await self.get_tasks(user_id, due_before=today, status="pending")
