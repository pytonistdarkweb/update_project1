from httpx import ASGITransport
import httpx
from sqlalchemy import text
from app.infrastructure.db import AsyncSessionLocal
import pytest
from unittest.mock import AsyncMock
from app.services.auth_services import UserAuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.essence.models.user import User
from app.infrastructure.repository.user_repo import UserWriteRepository
from app.services.token_creation_service import TokenService
from app.main import app




class MockUser:
    def __init__(self, id: int):
        self.id = id

@pytest.fixture
async def main_db_session():
    async with AsyncSessionLocal() as session:
        await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        await session.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;"))
        await session.commit()
        yield session  
        await session.rollback()  
        

@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    repo.get_user = AsyncMock()
    repo.create_user = AsyncMock()
    repo.session = AsyncMock()  
    return repo

@pytest.fixture
def auth_service(mock_user_repo):
    mock_session = AsyncMock()
    mock_user_repo.session = mock_session  
    return UserAuthService(session=mock_session)


@pytest.fixture
def task_data():
    return {
        "title": "New Task",
        "description": "Task description",
        "start_time": "2023-10-01T10:00:00",
        "end_time": "2023-10-01T11:00:00"
    }


def generate_valid_token():
    data = {"sub": "testuser"}
    access_token, _ = TokenService.create_tokens(data)
    return access_token


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture
def test_user():
    return {"id": 1, "username": "testuser", "email": "testuser@example.com"}