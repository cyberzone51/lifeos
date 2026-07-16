"""AI module — Router + Agents + Providers."""

from app.ai.router import ai_router, AIRouter, Intent
from app.ai.providers.gemini import gemini_provider, GeminiProvider
from app.ai.agents import finance_agent, health_agent, memory_agent

__all__ = [
    "ai_router",
    "AIRouter",
    "Intent",
    "gemini_provider",
    "GeminiProvider",
    "finance_agent",
    "health_agent",
    "memory_agent",
]
