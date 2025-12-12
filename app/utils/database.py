from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
        return cls.client

    @classmethod
    def get_master_db(cls):
        return cls.get_client()[settings.master_db_name]

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()