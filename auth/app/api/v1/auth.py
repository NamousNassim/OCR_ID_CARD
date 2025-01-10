from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, UserAuth, TwoFactorSetup, TwoFactorLogin
from app.services.auth import auth_service
from app.core.security import get_password_hash
from app.db.mongodb import db

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_auth: UserAuth):
    user_exists = await db.db.users.find_one({"email": user_auth.email})
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user_data = {
        "email": user_auth.email,
        "hashed_password": get_password_hash(user_auth.password),
        "is_active": True,
        "is_superuser": False,
        "two_factor_enabled": False
    }
    
    result = await db.db.users.insert_one(user_data)
    
    return {
        "access_token": auth_service.create_access_token(str(result.inserted_id)),
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="2FA required",
            headers={"X-2FA-Required": "true"}
        )
    
    return {
        "access_token": auth_service.create_access_token(str(user.id)),
        "token_type": "bearer"
    }

@router.post("/2fa/setup", response_model=dict)
async def setup_2fa(user_id: str):
    secret = await auth_service.setup_2fa(user_id)
    return {"secret": secret}

@router.post("/2fa/verify", response_model=Token)
async def verify_2fa(two_factor: TwoFactorLogin):
    user = await auth_service.authenticate_user(two_factor.email, two_factor.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not await auth_service.verify_2fa(str(user.id), two_factor.two_factor_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 2FA code"
        )
    
    return {
        "access_token": auth_service.create_access_token(str(user.id)),
        "token_type": "bearer"
    }