"""Integration tests for API endpoints — using in-memory SQLite."""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.main import app
from app.database.session import get_db, Base


# In-memory SQLite engine for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    loop = __import__("asyncio").get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create tables in memory for testing."""
    import app.models  # Import all models
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestTasksEndpoints:
    @pytest.mark.asyncio
    async def test_create_task(self, client):
        response = await client.post(
            "/api/v1/tasks/",
            json={"title": "Test task", "priority": 2},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test task"
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_list_tasks(self, client):
        response = await client.get("/api/v1/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestFinanceEndpoints:
    @pytest.mark.asyncio
    async def test_create_expense(self, client):
        response = await client.post(
            "/api/v1/finance/expenses",
            json={
                "amount": 100,
                "currency_code": "USD",
                "category_name": "food",
                "description": "Lunch",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["amount"] == 100

    @pytest.mark.asyncio
    async def test_list_expenses(self, client):
        response = await client.get("/api/v1/finance/expenses")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_statistics(self, client):
        response = await client.get("/api/v1/finance/statistics")
        assert response.status_code == 200
        data = response.json()
        assert "total_expenses" in data
        assert "total_income" in data
        assert "balance" in data


class TestAIEndpoints:
    @pytest.mark.asyncio
    async def test_memory_endpoint(self, client):
        response = await client.get("/api/v1/ai/memory")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_conversations_endpoint(self, client):
        response = await client.get("/api/v1/ai/conversations")
        assert response.status_code == 200


class TestGoalsEndpoints:
    @pytest.mark.asyncio
    async def test_create_goal(self, client):
        response = await client.post(
            "/api/v1/goals/",
            json={
                "title": "Save money",
                "category": "finance",
                "target_value": 10000,
                "unit": "USD",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Save money"
        assert data["category"] == "finance"

    @pytest.mark.asyncio
    async def test_list_goals(self, client):
        response = await client.get("/api/v1/goals/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestCalendarEndpoints:
    @pytest.mark.asyncio
    async def test_create_event(self, client):
        response = await client.post(
            "/api/v1/calendar/events",
            json={
                "title": "Meeting",
                "start_time": "2026-07-17T10:00:00",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Meeting"

    @pytest.mark.asyncio
    async def test_list_events(self, client):
        response = await client.get("/api/v1/calendar/events")
        assert response.status_code == 200


class TestFamilyEndpoints:
    @pytest.mark.asyncio
    async def test_create_family(self, client):
        response = await client.post(
            "/api/v1/family/",
            json={"name": "My Family"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My Family"
        assert "invite_code" in data

    @pytest.mark.asyncio
    async def test_list_families(self, client):
        response = await client.get("/api/v1/family/")
        assert response.status_code == 200


class TestGamificationEndpoints:
    @pytest.mark.asyncio
    async def test_get_level(self, client):
        response = await client.get("/api/v1/gamification/level")
        assert response.status_code == 200
        data = response.json()
        assert "level" in data
        assert "xp" in data

    @pytest.mark.asyncio
    async def test_add_xp(self, client):
        response = await client.post(
            "/api/v1/gamification/xp",
            params={"amount": 100},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["xp_added"] == 100


class TestCoachEndpoints:
    @pytest.mark.asyncio
    async def test_insights(self, client):
        response = await client.get("/api/v1/coach/insights")
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
