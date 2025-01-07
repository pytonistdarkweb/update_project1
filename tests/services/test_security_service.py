import pytest
from app.services.security_service import SecurityService

def test_get_password_hash():
    password = "mysecretpassword"
    hashed_password = SecurityService.get_password_hash(password)

    
    assert hashed_password != password
    
    assert SecurityService.verify_password(password, hashed_password)

def test_verify_password():
    password = "mysecretpassword"
    wrong_password = "wrongpassword"
    hashed_password = SecurityService.get_password_hash(password)

    
    assert SecurityService.verify_password(password, hashed_password)
    
    assert not SecurityService.verify_password(wrong_password, hashed_password)
