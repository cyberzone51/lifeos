"""Mental Wellness Service — ментальное здоровье."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.mental import StressLog, MeditationLog, GratitudeEntry
from app.models.health import MoodLog


class MentalWellnessService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_stress(
        self,
        user_id: uuid.UUID,
        level: int,
        source: str | None = None,
        notes: str | None = None,
    ) -> StressLog:
        log = StressLog(
            user_id=user_id,
            level=level,
            source=source,
            notes=notes,
        )
        self.db.add(log)
        await self.db.flush()
        return log

    async def log_meditation(
        self,
        user_id: uuid.UUID,
        duration_minutes: int,
        technique: str | None = None,
        notes: str | None = None,
    ) -> MeditationLog:
        log = MeditationLog(
            user_id=user_id,
            duration_minutes=duration_minutes,
            technique=technique,
            notes=notes,
        )
        self.db.add(log)
        await self.db.flush()
        return log

    async def log_gratitude(
        self,
        user_id: uuid.UUID,
        item1: str,
        item2: str,
        item3: str,
    ) -> GratitudeEntry:
        entry = GratitudeEntry(
            user_id=user_id,
            entry_date=datetime.utcnow(),
            item1=item1,
            item2=item2,
            item3=item3,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def get_stress_trend(self, user_id: uuid.UUID, days: int = 7) -> list[dict]:
        start_date = datetime.utcnow() - timedelta(days=days)
        query = (
            select(StressLog)
            .where(
                and_(
                    StressLog.user_id == user_id,
                    StressLog.logged_at >= start_date,
                )
            )
            .order_by(StressLog.logged_at)
        )
        result = await self.db.execute(query)
        logs = result.scalars().all()

        return [
            {
                "date": log.logged_at.isoformat(),
                "level": log.level,
                "source": log.source,
            }
            for log in logs
        ]

    async def get_meditation_stats(self, user_id: uuid.UUID) -> dict:
        query = select(func.sum(MeditationLog.duration_minutes)).where(
            MeditationLog.user_id == user_id
        )
        result = await self.db.execute(query)
        total_minutes = result.scalar() or 0

        week_ago = datetime.utcnow() - timedelta(days=7)
        week_query = select(func.count(MeditationLog.id)).where(
            and_(
                MeditationLog.user_id == user_id,
                MeditationLog.logged_at >= week_ago,
            )
        )
        week_result = await self.db.execute(week_query)
        week_sessions = week_result.scalar() or 0

        return {
            "total_minutes": total_minutes,
            "week_sessions": week_sessions,
            "average_per_day": round(total_minutes / max(7, 1), 1),
        }

    async def analyze_mood_correlation(self, user_id: uuid.UUID) -> dict:
        """Анализ связи сон → настроение → продуктивность."""
        # Get mood logs
        mood_query = select(MoodLog).where(MoodLog.user_id == user_id).order_by(MoodLog.logged_at.desc()).limit(30)
        mood_result = await self.db.execute(mood_query)
        mood_logs = mood_result.scalars().all()

        # Get sleep logs
        from app.models.health import SleepLog
        sleep_query = select(SleepLog).where(SleepLog.user_id == user_id).order_by(SleepLog.created_at.desc()).limit(30)
        sleep_result = await self.db.execute(sleep_query)
        sleep_logs = sleep_result.scalars().all()

        # Simple correlation analysis
        avg_mood = sum(m.mood for m in mood_logs) / len(mood_logs) if mood_logs else 5
        avg_sleep_quality = sum(s.quality or 3 for s in sleep_logs) / len(sleep_logs) if sleep_logs else 3

        correlation = "neutral"
        if avg_mood >= 7 and avg_sleep_quality >= 4:
            correlation = "positive"
        elif avg_mood <= 4 and avg_sleep_quality <= 2:
            correlation = "negative"

        return {
            "average_mood": round(avg_mood, 1),
            "average_sleep_quality": round(avg_sleep_quality, 1),
            "correlation": correlation,
            "recommendation": self._get_recommendation(correlation, avg_mood, avg_sleep_quality),
        }

    def _get_recommendation(self, correlation: str, mood: float, sleep: float) -> str:
        if correlation == "positive":
            return "Отлично! Хороший сон положительно влияет на твоё настроение. Продолжай!"
        elif correlation == "negative":
            return "Похоже, плохой сон влияет на настроение. Попробуй улучшить гигиену сна."
        else:
            return "Продолжай отслеживать, чтобы выявить закономерности."
