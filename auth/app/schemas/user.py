from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_superuser: bool
    two_factor_enabled: bool
    created_at: datetime
    updated_at: datetime