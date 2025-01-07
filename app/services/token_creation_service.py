from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status
from app.core.config import security_settings
from app.domain.essence.schemas.token import TokenData


SECRET_KEY = security_settings.SECRET_KEY
ALGORITHM = security_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = security_settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = security_settings.REFRESH_TOKEN_EXPIRE_DAYS


class TokenService:
    @staticmethod
    def create_tokens(data: dict) -> tuple[str, str]:
        
        
        access_token = TokenService._create_token(
            data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = TokenService._create_token(
            data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return access_token, refresh_token
    
    
    @staticmethod
    def _create_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            return TokenData(username=username)
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )