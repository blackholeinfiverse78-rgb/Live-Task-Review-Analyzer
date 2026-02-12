import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any

logger = logging.getLogger("task_review_system")

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None

    @classmethod
    async def connect(cls):
        uri = os.getenv("MONGODB_URI")
        if not uri:
            logger.warning("MONGODB_URI not found. System will fallback to in-memory storage (Not Persistent).")
            return
        
        try:
            cls.client = AsyncIOMotorClient(uri)
            cls.db = cls.client.get_default_database()
            # Verify connection
            await cls.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            cls.client = None
            cls.db = None

    @classmethod
    async def get_task(cls, task_id: str) -> Optional[Dict[str, Any]]:
        if cls.db is not None:
            return await cls.db.tasks.find_one({"task.task_id": task_id})
        return None

    @classmethod
    async def save_task(cls, task_id: str, data: Dict[str, Any]):
        if cls.db is not None:
            await cls.db.tasks.update_one(
                {"task.task_id": task_id},
                {"$set": data},
                upsert=True
            )

mongodb = MongoDB()
