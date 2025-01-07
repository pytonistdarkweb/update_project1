import pytest
from app.infrastructure.repository.user_repo import UserWriteRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

@pytest.mark.asyncio
async def test_create_user(main_db_session: AsyncSession):
    user_repo = UserWriteRepository(main_db_session)
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = await user_repo.create_user(
        username="testuser",
        email=unique_email,
        password_hash="hashedpassword"
    )
    assert user.username == "testuser"
    assert user.email == unique_email