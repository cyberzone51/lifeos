"""Gemini AI Provider — обёртка над Google Gemini API."""

import google.generativeai as genai
from typing import Optional
from app.core.config import settings


class GeminiProvider:
    """Провайдер для Google Gemini API."""

    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        else:
            self.model = None

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Генерация ответа через Gemini."""
        if not self.model:
            return "AI not configured. Set GEMINI_API_KEY in .env"

        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            if system_prompt:
                response = await self.model.generate_content_async(
                    prompt,
                    generation_config=generation_config,
                    system_instruction=system_prompt,
                )
            else:
                response = await self.model.generate_content_async(
                    prompt,
                    generation_config=generation_config,
                )

            return response.text
        except Exception as e:
            return f"AI error: {str(e)}"

    async def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Чат с историей сообщений."""
        if not self.model:
            return "AI not configured. Set GEMINI_API_KEY in .env"

        try:
            chat = self.model.start_chat(history=messages[:-1])
            response = await chat.send_message_async(
                messages[-1]["content"],
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                ),
            )
            return response.text
        except Exception as e:
            return f"AI error: {str(e)}"


# Singleton
gemini_provider = GeminiProvider()
