from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserModel(BaseModel):
    id: Optional[PyObjectId] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }