from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import user_service
from app.core.security import create_access_token
from .debs import get_current_user
from app.models.user import UserModel

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: UserModel = Depends(get_current_user)):
    """Get current user."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    """Update current user."""
    updated_user = await user_service.update_user(str(current_user.id), user_update)
    return updated_user

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    current_user: UserModel = Depends(get_current_user)
):
    """Get list of users. Only accessible by superusers."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    users = await user_service.get_users(skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    current_user: UserModel = Depends(get_current_user)
):
    """Create new user. Only accessible by superusers."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await user_service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Get user by ID. Only accessible by superusers."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    """Update user. Only accessible by superusers."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    updated_user = await user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Delete user. Only accessible by superusers."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}