"""Lightweight API tests — no database required."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealth:
    @pytest.mark.asyncio
    async def test_health(self, client):
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestTasks:
    @pytest.mark.asyncio
    async def test_create_task(self, client):
        r = await client.post("/api/v1/tasks/", json={"title": "Buy milk"})
        assert r.status_code == 200
        assert r.json()["title"] == "Buy milk"

    @pytest.mark.asyncio
    async def test_list_tasks(self, client):
        r = await client.get("/api/v1/tasks/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestFinance:
    @pytest.mark.asyncio
    async def test_statistics(self, client):
        r = await client.get("/api/v1/finance/statistics")
        assert r.status_code == 200
        assert "total_expenses" in r.json()
