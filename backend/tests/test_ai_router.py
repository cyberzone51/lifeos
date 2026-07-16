"""Tests for AI Router."""

import pytest
from app.ai.router import AIRouter, Intent


class TestIntent:
    """Tests for Intent dataclass."""

    def test_intent_creation(self):
        intent = Intent(category="finance", confidence=0.9, params={"amount": 100})
        assert intent.category == "finance"
        assert intent.confidence == 0.9
        assert intent.params["amount"] == 100

    def test_intent_default_params(self):
        intent = Intent(category="chat", confidence=0.5, params={})
        assert intent.params == {}


class TestAIRouter:
    """Tests for AIRouter."""

    @pytest.fixture
    def router(self):
        return AIRouter()

    def test_system_prompt_finance(self, router):
        prompt = router._get_system_prompt("finance")
        assert "финансовый" in prompt.lower() or "finance" in prompt.lower()

    def test_system_prompt_health(self, router):
        prompt = router._get_system_prompt("health")
        assert "здоровь" in prompt.lower() or "health" in prompt.lower()

    def test_system_prompt_reminder(self, router):
        prompt = router._get_system_prompt("reminder")
        assert "напоминан" in prompt.lower() or "remind" in prompt.lower()

    def test_system_prompt_chat(self, router):
        prompt = router._get_system_prompt("chat")
        assert "LifeOS" in prompt

    def test_system_prompt_unknown(self, router):
        prompt = router._get_system_prompt("unknown_category")
        assert "LifeOS" in prompt  # Falls back to chat

    def test_build_context_simple(self, router):
        intent = Intent(category="finance", confidence=0.9, params={"amount": 100})
        context = router._build_context("Потратил 100", intent)
        assert "finance" in context
        assert "100" in context

    def test_build_context_with_history(self, router):
        intent = Intent(category="chat", confidence=0.8, params={})
        history = [
            {"role": "user", "content": "Привет"},
            {"role": "assistant", "content": "Здравствуйте!"},
        ]
        context = router._build_context("Как дела?", intent, history)
        assert "История разговора" in context
        assert "Привет" in context
