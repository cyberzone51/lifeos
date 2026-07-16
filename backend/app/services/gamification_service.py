"""Gamification Service — уровни, достижения, XP."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.gamification import UserProgress, Achievement, UserAchievement, DailyChallenge


class GamificationService:
    # XP requirements per level
    XP_PER_LEVEL = {i: i * 100 for i in range(1, 100)}

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_progress(self, user_id: uuid.UUID) -> UserProgress:
        query = select(UserProgress).where(UserProgress.user_id == user_id)
        result = await self.db.execute(query)
        progress = result.scalar_one_or_none()
        
        if not progress:
            progress = UserProgress(user_id=user_id)
            self.db.add(progress)
            await self.db.flush()
        
        return progress

    async def add_xp(self, user_id: uuid.UUID, xp: int) -> UserProgress:
        progress = await self.get_or_create_progress(user_id)
        progress.xp += xp
        progress.total_xp += xp

        # Level up check
        while progress.level < 100:
            required = self.XP_PER_LEVEL.get(progress.level, 9999)
            if progress.xp >= required:
                progress.xp -= required
                progress.level += 1
            else:
                break

        await self.db.flush()
        return progress

    async def update_streak(self, user_id: uuid.UUID) -> UserProgress:
        progress = await self.get_or_create_progress(user_id)
        
        # Simple streak logic - in production, check actual activity dates
        today = datetime.utcnow().date()
        last_active = progress.updated_at.date() if progress.updated_at else None
        
        if last_active == today:
            pass  # Already counted today
        elif last_active == today - timedelta(days=1):
            progress.streak_days += 1
            if progress.streak_days > progress.longest_streak:
                progress.longest_streak = progress.streak_days
        else:
            progress.streak_days = 1

        await self.db.flush()
        return progress

    async def check_achievements(self, user_id: uuid.UUID) -> list[Achievement]:
        progress = await self.get_or_create_progress(user_id)
        
        # Get all achievements
        query = select(Achievement)
        result = await self.db.execute(query)
        all_achievements = result.scalars().all()

        # Get unlocked achievements
        unlocked_query = select(UserAchievement.achievement_id).where(
            UserAchievement.user_id == user_id
        )
        unlocked_result = await self.db.execute(unlocked_query)
        unlocked_ids = set(unlocked_result.scalars().all())

        new_achievements = []
        for achievement in all_achievements:
            if achievement.id in unlocked_ids:
                continue

            # Check requirement
            if achievement.requirement_type == "streak" and progress.streak_days >= achievement.requirement_value:
                new_achievements.append(achievement)
            elif achievement.requirement_type == "level" and progress.level >= achievement.requirement_value:
                new_achievements.append(achievement)

        return new_achievements

    async def unlock_achievement(self, user_id: uuid.UUID, achievement_id: uuid.UUID) -> bool:
        # Check if already unlocked
        existing = await self.db.execute(
            select(UserAchievement).where(
                and_(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_id == achievement_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            return False

        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
        )
        self.db.add(user_achievement)

        # Add XP reward
        achievement = await self.db.get(Achievement, achievement_id)
        if achievement:
            await self.add_xp(user_id, achievement.xp_reward)

        await self.db.flush()
        return True

    async def get_daily_challenges(self, user_id: uuid.UUID) -> list[DailyChallenge]:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        query = select(DailyChallenge).where(
            and_(
                DailyChallenge.user_id == user_id,
                DailyChallenge.challenge_date >= today,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_level_info(self, user_id: uuid.UUID) -> dict:
        progress = await self.get_or_create_progress(user_id)
        current_level_xp = self.XP_PER_LEVEL.get(progress.level, 9999)
        
        return {
            "level": progress.level,
            "xp": progress.xp,
            "xp_needed": current_level_xp,
            "xp_progress": progress.xp / current_level_xp if current_level_xp > 0 else 0,
            "total_xp": progress.total_xp,
            "streak": progress.streak_days,
            "longest_streak": progress.longest_streak,
        }
