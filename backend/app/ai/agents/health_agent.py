"""Health Agent — агент для работы со здоровьем."""

import json
from typing import Optional
from app.ai.providers.gemini import gemini_provider


class HealthAgent:
    """Агент для распознавания и создания записей о здоровье."""

    SYSTEM_PROMPT = """Ты — агент здоровья LifeOS.
Распознавай из текста:
- Тип активности: weight, sleep, walk, workout, water, mood
- Количественные данные (км, шаги, кг, часы, стаканы)
- Настроение (1-10)

Отвечай JSON:
{
  "activity_type": "walk",
  "value": 5,
  "unit": "km",
  "notes": "прогулка в парке"
}

Типы активности: weight, sleep, walk, run, workout, water, mood, steps
"""

    async def parse_activity(self, message: str) -> dict:
        """Парсинг активности из текста."""
        response = await gemini_provider.generate(
            prompt=f"Распознай активность: {message}",
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3,
        )

        try:
            data = json.loads(response)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_motivation(self, activity_type: str, streak: int) -> str:
        """Генерация мотивационного сообщения."""
        prompt = f"Пользователь сделал {activity_type}, streak: {streak} дней. Мотивируй кратко."
        
        return await gemini_provider.generate(
            prompt=prompt,
            system_prompt="Мотивируй кратко, дружелюбно, с эмодзи. 1-2 предложения.",
            temperature=0.8,
        )


# Singleton
health_agent = HealthAgent()
