import pytest
from datetime import timedelta
from jose import jwt
from app.services.token_creation_service import TokenService
from app.domain.essence.schemas.token import TokenData
from app.core.config import security_settings
from fastapi import HTTPException

SECRET_KEY = security_settings.SECRET_KEY
ALGORITHM = security_settings.ALGORITHM

def test_create_tokens():
    data = {"sub": "testuser"}
    access_token, refresh_token = TokenService.create_tokens(data)

    
    assert access_token is not None
    assert refresh_token is not None

    
    decoded_access_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    decoded_refresh_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_access_token["sub"] == "testuser"
    assert decoded_refresh_token["sub"] == "testuser"

def test_verify_token_success():
    data = {"sub": "testuser"}
    access_token, _ = TokenService.create_tokens(data)

    
    token_data = TokenService.verify_token(access_token)
    assert token_data.username == "testuser"

def test_verify_token_invalid():
    invalid_token = "invalid.token.string"

    
    with pytest.raises(HTTPException) as exc_info:
        TokenService.verify_token(invalid_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

def test_verify_token_expired():
    
    data = {"sub": "testuser"}
    expired_token = TokenService._create_token(data, timedelta(seconds=-1))

    
    with pytest.raises(HTTPException) as exc_info:
        TokenService.verify_token(expired_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
