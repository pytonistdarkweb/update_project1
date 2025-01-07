from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SecurityService:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
        
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)