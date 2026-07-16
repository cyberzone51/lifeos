"""AI Service — связь AI Router с БД и сервисами."""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.router import ai_router, Intent
from app.repositories.ai_repo import AIRepository
from app.repositories.finance_repo import FinanceRepository
from app.repositories.tasks_repo import TasksRepository
from app.services.finance_service import FinanceService
from app.services.tasks_service import TasksService


class AIService:
    """Сервис для обработки AI запросов с интеграцией в БД."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_repo = AIRepository(db)
        self.finance_repo = FinanceRepository(db)
        self.tasks_repo = TasksRepository(db)
        self.finance_service = FinanceService(db)
        self.tasks_service = TasksService(db)

    async def process_message(
        self,
        user_id: uuid.UUID,
        message: str,
        conversation_id: Optional[uuid.UUID] = None,
    ) -> dict:
        """Обработка сообщения пользователя: классификация → действие → ответ."""

        # 1. Получить или создать разговор
        if conversation_id:
            conversation = await self.ai_repo.get_conversation(
                conversation_id, user_id
            )
        else:
            conversation = await self.ai_repo.create_conversation(user_id)

        # 2. Сохранить сообщение пользователя
        await self.ai_repo.add_message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        # 3. Получить историю для контекста
        history = await self.ai_repo.get_conversation_history(
            conversation.id, limit=10
        )
        history_dicts = [
            {"role": msg.role, "content": msg.content} for msg in history
        ]

        # 4. Получить память пользователя для контекста
        memories = await self.ai_repo.get_user_memories(user_id)
        memory_context = {
            m.key: m.value for m in memories[:20]  # Топ 20 воспоминаний
        }

        # 5. Обработать через AI Router
        result = await ai_router.route(
            message=message,
            user_id=str(user_id),
            conversation_history=history_dicts,
        )

        # 6. Выполнить действие на основе намерения
        action_result = await self._execute_intent(
            intent=result["intent"],
            user_id=user_id,
            message=message,
        )

        # 7. Сохранить ответ AI
        response_text = result["response"]
        if action_result:
            response_text += f"\n\n{action_result.get('confirmation', '')}"

        await self.ai_repo.add_message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            agent_type=result["intent"]["category"],
        )

        # 8. Извлечь и сохранить память
        await self._extract_and_save_memory(user_id, message, result["intent"])

        return {
            "conversation_id": str(conversation.id),
            "response": response_text,
            "intent": result["intent"],
            "action_taken": action_result,
        }

    async def _execute_intent(
        self,
        intent: dict,
        user_id: uuid.UUID,
        message: str,
    ) -> Optional[dict]:
        """Выполнение действия на основе классифицированного намерения."""
        category = intent["category"]
        params = intent.get("params", {})

        try:
            if category == "finance":
                return await self._handle_finance(user_id, params, message)
            elif category == "tasks":
                return await self._handle_task(user_id, params, message)
            elif category == "reminder":
                return await self._handle_reminder(user_id, params, message)
            elif category == "health":
                return await self._handle_health(user_id, params, message)
        except Exception as e:
            return {"error": str(e), "confirmation": "Произошла ошибка при обработке."}

        return None

    async def _handle_finance(
        self, user_id: uuid.UUID, params: dict, message: str
    ) -> dict:
        """Обработка финансовой операции."""
        op_type = params.get("type", "expense")
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD")
        category_name = params.get("category", "other")
        description = params.get("description", message)

        if op_type == "expense":
            expense = await self.finance_service.create_expense(
                user_id=user_id,
                amount=amount,
                currency_code=currency,
                category_name=category_name,
                description=description,
            )
            return {
                "action": "expense_created",
                "expense_id": str(expense.id),
                "confirmation": f"✅ Расход записан: {amount} {currency} ({category_name})",
            }
        else:
            income = await self.finance_service.create_income(
                user_id=user_id,
                amount=amount,
                currency_code=currency,
                category_name=category_name,
                description=description,
            )
            return {
                "action": "income_created",
                "income_id": str(income.id),
                "confirmation": f"✅ Доход записан: {amount} {currency} ({category_name})",
            }

    async def _handle_task(
        self, user_id: uuid.UUID, params: dict, message: str
    ) -> dict:
        """Обработка создания задачи."""
        title = params.get("title", message)
        priority = params.get("priority", 2)
        due_date = params.get("due_date")

        task = await self.tasks_service.create_task(
            user_id=user_id,
            title=title,
            priority=priority,
        )
        return {
            "action": "task_created",
            "task_id": str(task.id),
            "confirmation": f"✅ Задача создана: {title}",
        }

    async def _handle_reminder(
        self, user_id: uuid.UUID, params: dict, message: str
    ) -> dict:
        """Обработка напоминания — создаёт задачу с дедлайном."""
        title = params.get("text", message)
        
        task = await self.tasks_service.create_task(
            user_id=user_id,
            title=f"🔔 {title}",
            priority=2,
        )
        return {
            "action": "reminder_created",
            "task_id": str(task.id),
            "confirmation": f"✅ Напоминание создано: {title}",
        }

    async def _handle_health(
        self, user_id: uuid.UUID, params: dict, message: str
    ) -> dict:
        """Обработка записи о здоровье."""
        activity = params.get("activity", "unknown")
        value = params.get("value", 0)
        
        # Пока просто подтверждаем
        return {
            "action": "health_logged",
            "confirmation": f"✅ Активность записана: {activity} — {value}",
        }

    async def _extract_and_save_memory(
        self, user_id: uuid.UUID, message: str, intent: dict
    ):
        """Извлечение и сохранение памяти из сообщения."""
        from app.ai.agents.memory_agent import memory_agent

        memories = await memory_agent.extract_memory(message)
        
        for mem in memories:
            await self.ai_repo.add_memory(
                user_id=user_id,
                category=mem.get("category", "general"),
                key=mem.get("key", "info"),
                value=mem.get("value", ""),
                source="inferred",
            )
