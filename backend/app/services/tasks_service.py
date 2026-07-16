"""Tasks Service — бизнес-логика задач."""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.repositories.tasks_repo import TasksRepository


class TasksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TasksRepository(db)

    async def create_task(
        self,
        user_id: uuid.UUID,
        title: str,
        description: str | None = None,
        priority: int = 2,
        due_date: datetime | None = None,
        tags: list[str] | None = None,
    ) -> Task:
        """Создание задачи."""
        task = await self.repo.create(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags,
        )
        return task

    async def complete_task(
        self, task_id: uuid.UUID, user_id: uuid.UUID
    ) -> Task | None:
        """Завершение задачи."""
        return await self.repo.complete(task_id, user_id)

    async def get_today_tasks(self, user_id: uuid.UUID) -> list[dict]:
        """Получение задач на сегодня."""
        tasks = await self.repo.get_today_tasks(user_id)
        return [
            {
                "id": str(t.id),
                "title": t.title,
                "priority": t.priority,
                "due_date": t.due_date.isoformat() if t.due_date else None,
            }
            for t in tasks
        ]

    async def get_tasks_by_priority(
        self, user_id: uuid.UUID
    ) -> dict[str, list[dict]]:
        """Получение задач, сгруппированных по приоритету."""
        all_tasks = await self.repo.get_tasks(user_id, status="pending")
        
        grouped = {"high": [], "medium": [], "low": []}
        for task in all_tasks:
            item = {
                "id": str(task.id),
                "title": task.title,
                "due_date": task.due_date.isoformat() if task.due_date else None,
            }
            if task.priority == 3:
                grouped["high"].append(item)
            elif task.priority == 2:
                grouped["medium"].append(item)
            else:
                grouped["low"].append(item)
        
        return grouped
