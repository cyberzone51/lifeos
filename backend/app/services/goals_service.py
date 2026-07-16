"""Goals Service — управление целями."""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.goals import Goal, GoalMilestone


class GoalsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_goal(
        self,
        user_id: uuid.UUID,
        title: str,
        category: str,
        description: str | None = None,
        target_value: float | None = None,
        unit: str | None = None,
        deadline: datetime | None = None,
    ) -> Goal:
        goal = Goal(
            user_id=user_id,
            title=title,
            category=category,
            description=description,
            target_value=target_value,
            unit=unit,
            deadline=deadline,
        )
        self.db.add(goal)
        await self.db.flush()
        return goal

    async def get_user_goals(self, user_id: uuid.UUID, status: str | None = None) -> list[Goal]:
        query = select(Goal).where(Goal.user_id == user_id)
        if status:
            query = query.where(Goal.status == status)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_progress(self, goal_id: uuid.UUID, value: float) -> Goal | None:
        query = select(Goal).where(Goal.id == goal_id)
        result = await self.db.execute(query)
        goal = result.scalar_one_or_none()
        
        if goal:
            goal.current_value = float(goal.current_value or 0) + value
            if goal.target_value and goal.current_value >= goal.target_value:
                goal.status = "completed"
            await self.db.flush()
        
        return goal

    async def complete_goal(self, goal_id: uuid.UUID) -> Goal | None:
        query = select(Goal).where(Goal.id == goal_id)
        result = await self.db.execute(query)
        goal = result.scalar_one_or_none()
        
        if goal:
            goal.status = "completed"
            await self.db.flush()
        
        return goal

    async def get_ai_breakdown(self, goal: Goal) -> dict:
        """AI разбивает цель на шаги."""
        if not goal.target_value or not goal.deadline:
            return {"steps": []}

        days_left = (goal.deadline - datetime.utcnow()).days
        if days_left <= 0:
            return {"steps": [], "message": "Deadline passed"}

        remaining = float(goal.target_value) - float(goal.current_value or 0)
        daily_target = remaining / days_left

        return {
            "goal": goal.title,
            "target": float(goal.target_value),
            "current": float(goal.current_value or 0),
            "remaining": remaining,
            "days_left": days_left,
            "daily_target": round(daily_target, 2),
            "unit": goal.unit or "",
            "message": f"Откладывай {round(daily_target, 2)} {goal.unit or ''} в день.",
        }
