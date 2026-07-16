"""API v1 Router — главный роутер API со всеми модулями."""

from fastapi import APIRouter

from app.api.v1 import ai, auth, finance, tasks
from app.api.v1.goals import router as goals_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.family import router as family_router
from app.api.v1.gamification import router as gamification_router
from app.api.v1.coach import router as coach_router

api_router = APIRouter()

# Core modules
api_router.include_router(auth.router)
api_router.include_router(ai.router)
api_router.include_router(finance.router)
api_router.include_router(tasks.router)

# Extended modules
api_router.include_router(goals_router)
api_router.include_router(calendar_router)
api_router.include_router(family_router)
api_router.include_router(gamification_router)
api_router.include_router(coach_router)


@api_router.get("/")
async def api_root():
    """Корневой эндпоинт API."""
    return {
        "service": "LifeOS API",
        "version": "1.0.0",
        "docs": "/docs",
        "modules": [
            "auth", "ai", "finance", "tasks",
            "goals", "calendar", "family", "gamification", "coach",
        ],
    }
