"""Gamification API — эндпоинты для геймификации."""

import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.gamification_service import GamificationService

router = APIRouter(prefix="/gamification", tags=["Gamification"])


class LevelResponse(BaseModel):
    level: int
    xp: int
    xp_needed: int
    xp_progress: float
    total_xp: int
    streak: int
    longest_streak: int


@router.get("/level", response_model=LevelResponse)
async def get_level(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = GamificationService(db)
    info = await service.get_level_info(user_id)
    return info


@router.post("/xp")
async def add_xp(
    amount: int,
    db: AsyncSession = Depends(get_db),
):
    user_id = uuid.uuid4()
    service = GamificationService(db)
    progress = await service.add_xp(user_id, amount)
    return {
        "status": "added",
        "xp_added": amount,
        "total_xp": progress.total_xp,
        "level": progress.level,
    }


@router.get("/achievements")
async def list_achievements(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = GamificationService(db)
    new_achievements = await service.check_achievements(user_id)
    
    return {
        "new_achievements": [
            {
                "id": str(a.id),
                "name": a.name,
                "description": a.description,
                "xp_reward": a.xp_reward,
            }
            for a in new_achievements
        ]
    }


@router.post("/achievements/{achievement_id}/unlock")
async def unlock_achievement(
    achievement_id: str,
    db: AsyncSession = Depends(get_db),
):
    user_id = uuid.uuid4()
    service = GamificationService(db)
    unlocked = await service.unlock_achievement(user_id, uuid.UUID(achievement_id))
    
    return {
        "status": "unlocked" if unlocked else "already_unlocked",
    }


@router.get("/challenges")
async def get_daily_challenges(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = GamificationService(db)
    challenges = await service.get_daily_challenges(user_id)
    
    return {
        "challenges": [
            {
                "id": str(c.id),
                "title": c.title,
                "xp_reward": c.xp_reward,
                "is_completed": c.is_completed,
            }
            for c in challenges
        ]
    }
