from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.essence.schemas.token import Token
from app.domain.essence.schemas.user import UserCreate
from app.services.auth_services import UserAuthService
from app.services.token_creation_service import TokenService
from app.services.auth_services import UserAuthService
from app.infrastructure.dependency import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.except_endpoints import UnauthorizedError

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/register", response_model=UserCreate)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    auth_service = UserAuthService(session)
    return await auth_service.create_user(user_data)



@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    auth_service = UserAuthService(session)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedError.raise_unauthorized_error()
    access_token, refresh_token = TokenService.create_tokens({"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token)