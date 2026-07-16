"""Tests for Mental Wellness Service."""

import pytest
from unittest.mock import AsyncMock
from app.services.mental_service import MentalWellnessService


class TestMentalWellnessService:
    """Tests for MentalWellnessService."""

    @pytest.fixture
    def mock_db(self):
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_db):
        return MentalWellnessService(mock_db)

    def test_recommendation_positive(self, service):
        rec = service._get_recommendation("positive", 8, 5)
        assert "Отлично" in rec or "хороший" in rec.lower()

    def test_recommendation_negative(self, service):
        rec = service._get_recommendation("negative", 3, 2)
        assert "сон" in rec.lower() or "улучшить" in rec.lower()

    def test_recommendation_neutral(self, service):
        rec = service._get_recommendation("neutral", 5, 3)
        assert "продолжай" in rec.lower() or "закономерност" in rec.lower()
