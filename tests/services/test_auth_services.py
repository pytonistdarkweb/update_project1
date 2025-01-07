import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.services.auth_services import UserAuthService
from app.domain.essence.schemas.user import UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_user_success():
    
    mock_repo = AsyncMock()
    mock_repo.get_user.return_value = None  
    mock_repo.create_user.return_value = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )

    
    with patch('app.services.auth_services.SecurityService.get_password_hash', return_value="hashedpassword"):
        
        auth_service = UserAuthService(session=AsyncMock())
        auth_service.user_repo = mock_repo

        
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        
        new_user = await auth_service.create_user(user_data)

        
        assert new_user.username == "testuser"
        assert new_user.email == "test@example.com"
        assert new_user.password == "password123"
        mock_repo.create_user.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_user_already_exists():
    
    mock_repo = AsyncMock()
    mock_repo.get_user.return_value = UserCreate(
        username="existinguser",
        email="existing@example.com",
        password="password123"
    )

    
    auth_service = UserAuthService(session=AsyncMock())
    auth_service.user_repo = mock_repo

    
    user_data = UserCreate(
        username="existinguser",
        email="existing@example.com",
        password="password123"
    )

    
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.create_user(user_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username or email already registered" 

@pytest.mark.asyncio
async def test_authenticate_user_success():
    
    mock_repo = AsyncMock()
    mock_repo.get_user.return_value = UserLogin(
        email="test@example.com",
        password="hashedpassword"
    )

    
    with patch('app.services.security_service.SecurityService.verify_password', return_value=True):
        
        auth_service = UserAuthService(session=AsyncMock())
        auth_service.user_repo = mock_repo

        
        authenticated_user = await auth_service.authenticate_user("test@example.com", "password123")

        
        assert authenticated_user is not None
        assert authenticated_user.email == "test@example.com"
        assert authenticated_user.password == "hashedpassword"


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password():
    
    mock_repo = AsyncMock()
    mock_repo.get_user.return_value = UserLogin(
        email="test@example.com",
        password="hashedpassword"
    )

    
    with patch('app.services.security_service.SecurityService.verify_password', return_value=False):
        
        auth_service = UserAuthService(session=AsyncMock())
        auth_service.user_repo = mock_repo

        
        authenticated_user = await auth_service.authenticate_user("test@example.com", "wrongpassword")

        
        assert authenticated_user is None

@pytest.mark.asyncio
async def test_authenticate_user_not_found():
    
    mock_repo = AsyncMock()
    mock_repo.get_user.return_value = None  

    
    auth_service = UserAuthService(session=AsyncMock())
    auth_service.user_repo = mock_repo

    
    authenticated_user = await auth_service.authenticate_user("nonexistent@example.com", "hashedpassword")

    
    assert authenticated_user is None


