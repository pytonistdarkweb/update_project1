from pydantic_settings import BaseSettings
from typing import List


class BaseAppSettings(BaseSettings):
    """Базовый класс с общей конфигурацией"""
    class Config:
        case_sensitive = True  


class Settings(BaseAppSettings):
    """Core application settings"""
    PROJECT_NAME: str = "Task Management API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API for managing tasks with translation support"
    DEBUG: bool = True


class DatabaseSettings(BaseAppSettings):
    """Database connection settings"""
    DATABASE_URL: str ="postgresql+asyncpg://postgres:postgres@localhost:5433/postgres"
    DEBUG: bool = False
    

class ServerSettings(BaseAppSettings):
    """Server configuration settings"""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

class SecuritySettings(BaseAppSettings):
    """Security and authentication settings"""
    SECRET_KEY: str = "05d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e8"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class CorsSettings(BaseAppSettings):
    """CORS configuration settings"""
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000"
    ]


settings = Settings()
db_settings = DatabaseSettings()
server_settings = ServerSettings()
security_settings = SecuritySettings()
cors_settings = CorsSettings()