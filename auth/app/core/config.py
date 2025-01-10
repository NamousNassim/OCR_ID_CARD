from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "auth_service"
    JWT_SECRET_KEY: str = "jwtizdabest"  
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_2FA_KEY: str = "test2fa"  

    class Config:
        env_file = ".env"

settings = Settings()