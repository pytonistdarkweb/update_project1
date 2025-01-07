from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.token_creation_service import TokenService
from app.services.auth_services import UserAuthService
from app.infrastructure.dependency import get_db
from app.infrastructure.repository.user_repo import UserWriteRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = TokenService.verify_token(token)
        if token_data.username is None:
            raise credentials_exception
    except:
        raise credentials_exception
        
    async with get_db() as session:
        user_repo = UserWriteRepository(session)
        auth_service = UserAuthService(user_repo)
        user = await auth_service.get_user(token_data.username)
        if user is None:
            raise credentials_exception
        return user 