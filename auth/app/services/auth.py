from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token, create_totp_secret, verify_totp
from app.db.mongodb import db
from app.models.user import UserModel
from app.core.config import settings

class AuthService:
    async def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        user_doc = await db.db.users.find_one({"email": email})
        if not user_doc:
            return None
        user = UserModel(**user_doc)
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, user_id: str) -> str:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(user_id, expires_delta)

    async def setup_2fa(self, user_id: str) -> str:
        secret = create_totp_secret()
        await db.db.users.update_one(
            {"_id": user_id},
            {"$set": {"two_factor_secret": secret, "two_factor_enabled": False}}
        )
        return secret

    async def verify_2fa(self, user_id: str, code: str) -> bool:
        user_doc = await db.db.users.find_one({"_id": user_id})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        user = UserModel(**user_doc)
        if not user.two_factor_secret:
            raise HTTPException(status_code=400, detail="2FA not set up")
        return verify_totp(user.two_factor_secret, code)

auth_service = AuthService()