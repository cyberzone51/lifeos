"""Goals API — эндпоинты для целей."""

import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.goals_service import GoalsService

router = APIRouter(prefix="/goals", tags=["Goals"])


class GoalCreate(BaseModel):
    title: str
    category: str  # health, finance, education, personal
    description: Optional[str] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    deadline: Optional[datetime] = None


class GoalResponse(BaseModel):
    id: str
    title: str
    category: str
    description: Optional[str]
    target_value: Optional[float]
    current_value: Optional[float]
    unit: Optional[str]
    deadline: Optional[datetime]
    status: str
    progress: float


@router.post("/", response_model=GoalResponse)
async def create_goal(request: GoalCreate, db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = GoalsService(db)
    
    goal = await service.create_goal(
        user_id=user_id,
        title=request.title,
        category=request.category,
        description=request.description,
        target_value=request.target_value,
        unit=request.unit,
        deadline=request.deadline,
    )
    
    progress = float(goal.current_value or 0) / float(goal.target_value or 1) * 100
    
    return GoalResponse(
        id=str(goal.id),
        title=goal.title,
        category=goal.category,
        description=goal.description,
        target_value=goal.target_value,
        current_value=goal.current_value,
        unit=goal.unit,
        deadline=goal.deadline,
        status=goal.status,
        progress=min(progress, 100),
    )


@router.get("/", response_model=List[GoalResponse])
async def list_goals(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    user_id = uuid.uuid4()
    service = GoalsService(db)
    goals = await service.get_user_goals(user_id, status)
    
    return [
        GoalResponse(
            id=str(g.id),
            title=g.title,
            category=g.category,
            description=g.description,
            target_value=g.target_value,
            current_value=g.current_value,
            unit=g.unit,
            deadline=g.deadline,
            status=g.status,
            progress=min(float(g.current_value or 0) / float(g.target_value or 1) * 100, 100),
        )
        for g in goals
    ]


@router.post("/{goal_id}/progress")
async def update_progress(
    goal_id: str,
    value: float,
    db: AsyncSession = Depends(get_db),
):
    service = GoalsService(db)
    goal = await service.update_progress(uuid.UUID(goal_id), value)
    
    if not goal:
        return {"error": "Goal not found"}
    
    return {
        "status": "updated",
        "current_value": float(goal.current_value),
        "target_value": float(goal.target_value) if goal.target_value else None,
    }


@router.get("/{goal_id}/breakdown")
async def get_ai_breakdown(goal_id: str, db: AsyncSession = Depends(get_db)):
    """AI разбивает цель на шаги."""
    service = GoalsService(db)
    from sqlalchemy import select
    from app.models.goals import Goal
    
    query = select(Goal).where(Goal.id == uuid.UUID(goal_id))
    result = await db.execute(query)
    goal = result.scalar_one_or_none()
    
    if not goal:
        return {"error": "Goal not found"}
    
    breakdown = await service.get_ai_breakdown(goal)
    return breakdown
