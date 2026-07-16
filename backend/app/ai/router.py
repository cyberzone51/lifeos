"""AI Router — центральный маршрутизатор сообщений."""

import json
from typing import Optional
from dataclasses import dataclass

from app.ai.providers.gemini import gemini_provider


@dataclass
class Intent:
    category: str  # finance, health, reminder, planner, knowledge, chat
    confidence: float
    params: dict


class AIRouter:
    """
    Классифицирует входящее сообщение и направляет в нужного агента.
    """

    CLASSIFICATION_PROMPT = """Ты — AI классификатор намерений. 
Проанализируй сообщение пользователя и определи:
1. category: finance | health | reminder | planner | knowledge | chat
2. confidence: 0.0-1.0
3. params: извлечённые параметры

Примеры:
- "Потратил 200 CZK на еду" → {"category": "finance", "confidence": 0.95, "params": {"type": "expense", "amount": 200, "currency": "CZK", "category": "food"}}
- "Прошёл 5 км" → {"category": "health", "confidence": 0.9, "params": {"activity": "walking", "distance_km": 5}}
- "Напомни завтра в 9" → {"category": "reminder", "confidence": 0.95, "params": {"time": "tomorrow 09:00"}}
- "Привет" → {"category": "chat", "confidence": 0.99, "params": {}}

Ответ ТОЛЬКО в JSON формате: {"category": "...", "confidence": ..., "params": {...}}
"""

    def __init__(self):
        self.providers = {
            "gemini": gemini_provider,
        }
        self._default_provider = "gemini"

    async def classify(self, message: str) -> Intent:
        """Классификация намерения сообщения."""
        provider = self.providers[self._default_provider]

        response = await provider.generate(
            prompt=f"Сообщение: {message}",
            system_prompt=self.CLASSIFICATION_PROMPT,
            temperature=0.3,
        )

        try:
            # Парсим JSON из ответа
            data = json.loads(response)
            return Intent(
                category=data.get("category", "chat"),
                confidence=data.get("confidence", 0.5),
                params=data.get("params", {}),
            )
        except (json.JSONDecodeError, KeyError):
            return Intent(category="chat", confidence=0.5, params={})

    async def route(
        self,
        message: str,
        user_id: str,
        conversation_history: Optional[list] = None,
    ) -> dict:
        """
        Маршрутизация сообщения: классификация → агент → ответ.
        """
        # 1. Классификация
        intent = await self.classify(message)

        # 2. Выбор промпта на основе категории
        system_prompt = self._get_system_prompt(intent.category)

        # 3. Формирование контекста
        context = self._build_context(message, intent, conversation_history)

        # 4. Генерация ответа
        provider = self.providers[self._default_provider]
        response = await provider.generate(
            prompt=context,
            system_prompt=system_prompt,
            temperature=0.7,
        )

        return {
            "response": response,
            "intent": {
                "category": intent.category,
                "confidence": intent.confidence,
                "params": intent.params,
            },
            "action_taken": await self._execute_action(intent, user_id),
        }

    def _get_system_prompt(self, category: str) -> str:
        """Системный промпт для каждой категории."""
        prompts = {
            "finance": """Ты — AI финансовый ассистент LifeOS.
Пользователь сообщает о расходе/доходе. Отвечай кратко и по делу.
Подтверди запись и покажи итог. Используй эмодзи для категорий.""",
            
            "health": """Ты — AI помощник по здоровью LifeOS.
Пользователь сообщает о активности (ходьба, тренировка, вода, сон).
Отвечай мотивирующе и кратко. Поздравляй с достижениями.""",
            
            "reminder": """Ты — AI помощник для напоминаний LifeOS.
Пользователь просит напомнить о чём-то. Подтверди время и событие.
Будь точным в датах и времени.""",
            
            "planner": """Ты — AI помощник для задач LifeOS.
Пользователь создаёт задачу или спрашивает о планах.
Помогай с формулировками и дедлайнами.""",
            
            "knowledge": """Ты — AI помощник для базы знаний LifeOS.
Пользователь хочет сохранить информацию. Помогай с тегами и резюме.""",
            
            "chat": """Ты — LifeOS AI ассистент. Дружелюбный, полезный, краткий.
Помогаешь с повседневными задачами. Помни контекст разговора.""",
        }
        return prompts.get(category, prompts["chat"])

    def _build_context(
        self,
        message: str,
        intent: Intent,
        history: Optional[list] = None,
    ) -> str:
        """Построение контекста для AI."""
        parts = [f"Намерение: {intent.category} (уверенность: {intent.confidence})"]
        
        if intent.params:
            parts.append(f"Параметры: {json.dumps(intent.params, ensure_ascii=False)}")
        
        if history:
            parts.append("История разговора:")
            for msg in history[-5:]:  # Последние 5 сообщений
                parts.append(f"  {msg['role']}: {msg['content']}")
        
        parts.append(f"\nСообщение пользователя: {message}")
        
        return "\n".join(parts)

    async def _execute_action(self, intent: Intent, user_id: str) -> Optional[dict]:
        """Выполнение действия на основе намерения."""
        # TODO: Интеграция с сервисами для создания записей
        # Пока возвращаем mock
        if intent.category == "finance":
            return {"action": "expense_created", "params": intent.params}
        elif intent.category == "reminder":
            return {"action": "reminder_created", "params": intent.params}
        elif intent.category == "planner":
            return {"action": "task_created", "params": intent.params}
        
        return None


# Singleton
ai_router = AIRouter()
