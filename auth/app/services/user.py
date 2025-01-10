from typing import Optional, List
from fastapi import HTTPException, status
from bson import ObjectId
from app.db.mongodb import db
from app.models.user import UserModel
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """Get a user by ID."""
        try:
            user_doc = await db.db.users.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return UserModel(**user_doc)
        except:
            return None
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get a user by email."""
        user_doc = await db.db.users.find_one({"email": email})
        if user_doc:
            return UserModel(**user_doc)
        return None

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserModel]:
        """Get a list of users."""
        users = []
        cursor = db.db.users.find().skip(skip).limit(limit)
        async for user_doc in cursor:
            users.append(UserModel(**user_doc))
        return users

    async def create_user(self, user: UserCreate) -> UserModel:
        """Create a new user."""
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_dict = user.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        
        result = await db.db.users.insert_one(user_dict)
        created_user = await self.get_user_by_id(str(result.inserted_id))
        return created_user

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserModel]:
        """Update a user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return user

        if "email" in update_data:
            existing_user = await self.get_user_by_email(update_data["email"])
            if existing_user and str(existing_user.id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        await db.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        result = await db.db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

user_service = UserService()