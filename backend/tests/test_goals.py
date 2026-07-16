"""Tests for Goals Service."""

import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from app.services.goals_service import GoalsService
from app.models.goals import Goal


class TestGoalsService:
    """Tests for GoalsService."""

    @pytest.fixture
    def mock_db(self):
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_db):
        return GoalsService(mock_db)

    @pytest.fixture
    def sample_goal(self):
        return Goal(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            title="Save 100000",
            category="finance",
            target_value=100000,
            current_value=50000,
            unit="CZK",
            deadline=datetime.utcnow() + timedelta(days=180),
            status="active",
        )

    def test_ai_breakdown_calculation(self, service, sample_goal):
        breakdown = asyncio.run(service.get_ai_breakdown(sample_goal))
        
        assert breakdown["target"] == 100000
        assert breakdown["current"] == 50000
        assert breakdown["remaining"] == 50000
        assert breakdown["days_left"] > 0
        assert breakdown["daily_target"] > 0
        assert "280" in str(breakdown["daily_target"]) or "Откладывай" in breakdown["message"]

    def test_ai_breakdown_no_deadline(self, service):
        goal = Goal(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            title="Test",
            category="health",
            status="active",
        )
        breakdown = asyncio.run(service.get_ai_breakdown(goal))
        assert breakdown["steps"] == []

    def test_ai_breakdown_expired_deadline(self, service):
        goal = Goal(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            title="Test",
            category="health",
            target_value=100,
            deadline=datetime.utcnow() - timedelta(days=1),
            status="active",
        )
        breakdown = asyncio.run(service.get_ai_breakdown(goal))
        assert "Deadline passed" in breakdown.get("message", "")


import asyncio
