"""Finance Agent — агент для работы с финансами."""

from typing import Optional
from app.ai.providers.gemini import gemini_provider


class FinanceAgent:
    """Агент для распознавания и создания финансовых записей."""

    SYSTEM_PROMPT = """Ты — финансовый агент LifeOS. 
Распознавай из текста:
- Тип операции: expense (расход) или income (доход)
- Сумму и валюту
- Категорию (еда, транспорт, развлечения, зарплата, фриланс и т.д.)
- Описание

Отвечай JSON:
{
  "type": "expense|income",
  "amount": 200,
  "currency": "CZK",
  "category": "food",
  "description": "обед в ресторане",
  "tags": ["ресторан", "обед"]
}

Категории расходов: food, transport, entertainment, shopping, health, education, utilities, other
Категории доходов: salary, freelance, investment, gift, other
"""

    async def parse_expense(self, message: str) -> dict:
        """Парсинг финансовой операции из текста."""
        response = await gemini_provider.generate(
            prompt=f"Распознай финансовую операцию: {message}",
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3,
        )

        try:
            import json
            data = json.loads(response)
            return {
                "success": True,
                "data": data,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_response": response,
            }

    async def get_category_suggestion(
        self, description: str, history: Optional[list] = None
    ) -> str:
        """Предложение категории на основе описания."""
        prompt = f"Предложи категорию для: {description}"
        if history:
            prompt += f"\nИстория категорий: {', '.join(history[-10:])}"

        response = await gemini_provider.generate(
            prompt=prompt,
            system_prompt="Ответь ТОЛЬКО названием категории на английском (food, transport, etc).",
            temperature=0.3,
        )
        return response.strip().lower()


# Singleton
finance_agent = FinanceAgent()
