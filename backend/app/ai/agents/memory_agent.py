"""Memory Agent — агент для управления AI памятью."""

import json
from typing import Optional
from app.ai.providers.gemini import gemini_provider


class MemoryAgent:
    """Агент для извлечения и управления памятью пользователя."""

    EXTRACTION_PROMPT = """Извлеки информацию о пользователе из сообщения.
Категории: preferences, goals, dates, habits, style, personal

Примеры:
- "Я вегетарианец" → {"category": "preferences", "key": "diet", "value": "vegetarian"}
- "Мой день рождения 15 марта" → {"category": "dates", "key": "birthday", "value": "2000-03-15"}
- "Я люблю кофе" → {"category": "preferences", "key": "favorite_drink", "value": "coffee"}

Ответ JSON: [{"category": "...", "key": "...", "value": "..."}]
Если нет информации для запоминания, верни: []
"""

    async def extract_memory(self, message: str) -> list[dict]:
        """Извлечение информации для памяти из сообщения."""
        response = await gemini_provider.generate(
            prompt=f"Сообщение: {message}",
            system_prompt=self.EXTRACTION_PROMPT,
            temperature=0.3,
        )

        try:
            data = json.loads(response)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    async def recall_context(
        self, user_id: str, memories: list[dict], current_topic: str
    ) -> str:
        """Формирование контекста из памяти для персонализации."""
        if not memories:
            return ""

        memory_text = "\n".join(
            f"- {m['key']}: {m['value']}" for m in memories
        )

        prompt = f"""Используй эту информацию о пользователе для персонализации ответа:
{memory_text}

Текущая тема: {current_topic}

Сформируй краткий контекст (2-3 предложения)."""

        return await gemini_provider.generate(
            prompt=prompt,
            system_prompt="Будь кратким, только факты для контекста.",
            temperature=0.3,
        )


# Singleton
memory_agent = MemoryAgent()
