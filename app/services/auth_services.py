from typing import Optional
from app.infrastructure.repository.user_repo import UserWriteRepository
from app.domain.essence.schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.services.security_service import SecurityService

class UserAuthService:

    def __init__(self, session: AsyncSession):
        self.user_repo = UserWriteRepository(session)

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repo.get_user(
            username=user_data.username, 
            email=user_data.email
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        hashed_password = SecurityService.get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        return await self.user_repo.create_user(new_user)
    

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_user(username=username)
        if not user or not SecurityService.verify_password(password, user.password):
            return None
        return user
    