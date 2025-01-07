import pytest
from fastapi.testclient import TestClient
from app.main import app  
from app.services.auth_services import UserAuthService
from unittest.mock import AsyncMock, patch

client = TestClient(app)

class MockUser:
    def __init__(self, username):
        self.username = username

@pytest.mark.asyncio
async def test_register_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }

    
    with patch.object(UserAuthService, 'create_user', return_value=user_data):
        response = client.post("/register", json=user_data)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_success():
    form_data = {
        "username": "testuser",
        "password": "password123"
    }

    with patch.object(UserAuthService, 'authenticate_user', return_value=MockUser("testuser")):
        response = client.post("/login", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


