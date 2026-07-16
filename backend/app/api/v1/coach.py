"""Life Coach API — AI тренер жизни."""

import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.life_coach_service import AILifeCoach

router = APIRouter(prefix="/coach", tags=["AI Life Coach"])


@router.get("/briefing")
async def get_daily_briefing(db: AsyncSession = Depends(get_db)):
    """Утренний брифинг от AI."""
    user_id = uuid.uuid4()
    coach = AILifeCoach(db)
    briefing = await coach.get_daily_briefing(user_id)
    return briefing


@router.get("/weekly")
async def get_weekly_analysis(db: AsyncSession = Depends(get_db)):
    """Недельный анализ."""
    user_id = uuid.uuid4()
    coach = AILifeCoach(db)
    analysis = await coach.get_weekly_analysis(user_id)
    return analysis


@router.get("/insights")
async def get_insights(db: AsyncSession = Depends(get_db)):
    """AI инсайты."""
    user_id = uuid.uuid4()
    coach = AILifeCoach(db)
    insights = await coach.get_insights(user_id)
    return {"insights": insights}


@router.get("/recommendation")
async def get_recommendation(
    topic: str = "general",
    db: AsyncSession = Depends(get_db),
):
    """Персональная рекомендация по теме."""
    from app.ai.providers.gemini import gemini_provider
    
    coach = AILifeCoach(db)
    
    # Get user data
    level_info = await coach.gamification_service.get_level_info(uuid.uuid4())
    
    prompt = f"""
Дай персональную рекомендацию по теме: {topic}

Данные пользователя:
- Уровень: {level_info['level']}
- Streak: {level_info['streak']} дней
"""
    
    response = await gemini_provider.generate(
        prompt=prompt,
        system_prompt="Дай 1-2 конкретные рекомендации. Будь мотивирующим.",
        temperature=0.7,
    )
    
    return {"recommendation": response}
