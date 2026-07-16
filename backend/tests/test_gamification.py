"""Tests for Gamification Service."""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.gamification_service import GamificationService


class TestGamificationService:
    """Tests for GamificationService."""

    @pytest.fixture
    def mock_db(self):
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_db):
        return GamificationService(mock_db)

    def test_xp_per_level(self, service):
        assert service.XP_PER_LEVEL[1] == 100
        assert service.XP_PER_LEVEL[2] == 200
        assert service.XP_PER_LEVEL[10] == 1000

    def test_level_calculation(self, service):
        # Level 1 needs 100 XP
        assert service.XP_PER_LEVEL[1] == 100

    def test_xp_per_level_scales(self, service):
        # XP requirement scales linearly
        assert service.XP_PER_LEVEL[5] == 500
        assert service.XP_PER_LEVEL[20] == 2000
