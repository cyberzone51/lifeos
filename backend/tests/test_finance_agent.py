"""Tests for Finance Agent."""

import pytest
from app.ai.agents.finance_agent import FinanceAgent


class TestFinanceAgent:
    """Tests for FinanceAgent."""

    @pytest.fixture
    def agent(self):
        return FinanceAgent()

    def test_system_prompt_contains_categories(self, agent):
        assert "food" in agent.SYSTEM_PROMPT.lower()
        assert "transport" in agent.SYSTEM_PROMPT.lower()
        assert "salary" in agent.SYSTEM_PROMPT.lower()

    def test_system_prompt_json_format(self, agent):
        assert "JSON" in agent.SYSTEM_PROMPT
