from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_mongo(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        try:
            
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(f"Unable to connect to MongoDB: {e}")
            raise e

    async def close_mongo_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

 
db = MongoDB()
 
async def connect_to_mongo():
    await db.connect_to_mongo()

async def close_mongo_connection():
    await db.close_mongo_connection()