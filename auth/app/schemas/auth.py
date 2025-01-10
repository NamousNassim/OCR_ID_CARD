from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class TwoFactorSetup(BaseModel):
    two_factor_code: str

class TwoFactorLogin(BaseModel):
    email: EmailStr
    password: str
    two_factor_code: str