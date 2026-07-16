"""AI Life Coach — персональный тренер жизни."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.providers.gemini import gemini_provider
from app.repositories.finance_repo import FinanceRepository
from app.repositories.tasks_repo import TasksRepository
from app.repositories.ai_repo import AIRepository
from app.services.goals_service import GoalsService
from app.services.gamification_service import GamificationService


class AILifeCoach:
    """AI анализирует все аспекты жизни и даёт рекомендации."""

    SYSTEM_PROMPT = """Ты — AI Life Coach в приложении LifeOS.
Анализируй данные пользователя и давай персонализированные рекомендации.

Данные включают:
- Финансы (расходы, доходы, бюджет)
- Задачи (выполненные, просроченные)
- Привычки (streak, прогресс)
- Цели (прогресс, дедлайны)
- Здоровье (сон, вес, настроение)

Правила:
- Будь конкретным, используй цифры
- Давай actionable советы (1-3 предложения)
- Мотивируй, но честно
- Используй эмодзи для читаемости
"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.finance_repo = FinanceRepository(db)
        self.tasks_repo = TasksRepository(db)
        self.ai_repo = AIRepository(db)
        self.goals_service = GoalsService(db)
        self.gamification_service = GamificationService(db)

    async def get_daily_briefing(self, user_id: uuid.UUID) -> dict:
        """Утренний брифинг: задачи, привычки, расходы."""
        # Get today's tasks
        tasks = await self.tasks_repo.get_today_tasks(user_id)
        
        # Get recent expenses
        from datetime import datetime
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        expenses = await self.finance_repo.get_expenses(user_id, week_ago, now, limit=5)
        
        # Get goals
        goals = await self.goals_service.get_user_goals(user_id, "active")
        
        # Get level info
        level_info = await self.gamification_service.get_level_info(user_id)

        # Build context for AI
        context = f"""
Данные пользователя на {now.strftime('%d.%m.%Y')}:

Задачи на сегодня ({len(tasks)}):
{chr(10).join(f"- {t.title} (приоритет: {t.priority})" for t in tasks[:5])}

Последние расходы за неделю:
{chr(10).join(f"- {e.description or 'Без описания'}: {e.amount} {e.currency_code}" for e in expenses[:5])}

Активные цели ({len(goals)}):
{chr(10).join(f"- {g.title}: {g.current_value}/{g.target_value} {g.unit or ''}" for g in goals[:3])}

Уровень: {level_info['level']}, streak: {level_info['streak']} дней
"""

        response = await gemini_provider.generate(
            prompt=f"Составь утренний брифинг:\n{context}",
            system_prompt=self.SYSTEM_PROMPT + "\n\nФормат: краткий, структурированный, 3-5 пунктов.",
            temperature=0.7,
        )

        return {
            "date": now.strftime("%d.%m.%Y"),
            "tasks_count": len(tasks),
            "goals_count": len(goals),
            "level": level_info["level"],
            "streak": level_info["streak"],
            "briefing": response,
        }

    async def get_weekly_analysis(self, user_id: uuid.UUID) -> dict:
        """Недельный анализ: что изменилось."""
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        two_weeks_ago = now - timedelta(days=14)

        # This week expenses
        this_week_expenses = await self.finance_repo.get_expenses_total(
            user_id, week_ago, now
        )
        last_week_expenses = await self.finance_repo.get_expenses_total(
            user_id, two_weeks_ago, week_ago
        )

        # This week tasks
        this_week_tasks = await self.tasks_repo.get_tasks(user_id, "completed")
        
        # Goals progress
        goals = await self.goals_service.get_user_goals(user_id, "active")

        context = f"""
Недельный анализ:

Финансы:
- Эта неделя: {this_week_expenses} 
- Прошлая неделя: {last_week_expenses}
- Изменение: {((this_week_expenses - last_week_expenses) / max(last_week_expenses, 1) * 100):.0f}%

Задачи выполнено: {len(this_week_tasks)}

Цели:
{chr(10).join(f"- {g.title}: {g.current_value}/{g.target_value}" for g in goals[:5])}
"""

        response = await gemini_provider.generate(
            prompt=f"Проанализируй неделю:\n{context}",
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.7,
        )

        return {
            "period": f"{week_ago.strftime('%d.%m')} - {now.strftime('%d.%m')}",
            "expenses_change": float(this_week_expenses) - float(last_week_expenses),
            "tasks_completed": len(this_week_tasks),
            "analysis": response,
        }

    async def get_insights(self, user_id: uuid.UUID) -> list[dict]:
        """AI инсайты на основе всех данных."""
        now = datetime.utcnow()
        month_ago = now - timedelta(days=30)

        # Gather data
        expenses = await self.finance_repo.get_expenses(user_id, month_ago, now, limit=100)
        goals = await self.goals_service.get_user_goals(user_id)
        level_info = await self.gamification_service.get_level_info(user_id)

        insights = []

        # Finance insight
        if expenses:
            total = sum(float(e.amount) for e in expenses)
            insights.append({
                "type": "finance",
                "icon": "💰",
                "title": "Расходы за месяц",
                "value": f"{total:.0f}",
                "detail": f"{len(expenses)} транзакций",
            })

        # Goals insight
        active_goals = [g for g in goals if g.status == "active"]
        if active_goals:
            completed = sum(1 for g in active_goals if g.current_value and g.target_value and float(g.current_value) >= float(g.target_value))
            insights.append({
                "type": "goals",
                "icon": "🎯",
                "title": "Цели",
                "value": f"{completed}/{len(active_goals)}",
                "detail": "достигнуто",
            })

        # Level insight
        insights.append({
            "type": "level",
            "icon": "🏆",
            "title": "Уровень",
            "value": str(level_info["level"]),
            "detail": f"streak: {level_info['streak']} дней",
        })

        return insights
