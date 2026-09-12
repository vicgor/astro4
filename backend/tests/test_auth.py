import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.database import engine
from app.main import app
from app.models.user import Base


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        register_response = await ac.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "secret123"},
        )
        assert register_response.status_code == 201

        login_response = await ac.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "secret123"},
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()
