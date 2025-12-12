from app.utils.database import Database
from typing import List


class CollectionService:
    @staticmethod
    async def create_organization_collection(collection_name: str) -> bool:
        try:
            db = Database.get_master_db()
            await db.create_collection(collection_name)
            return True
        except Exception as e:
            raise Exception(f"Failed to create collection: {str(e)}")

    @staticmethod
    async def drop_organization_collection(collection_name: str) -> bool:
        try:
            db = Database.get_master_db()
            await db.drop_collection(collection_name)
            return True
        except Exception as e:
            raise Exception(f"Failed to drop collection: {str(e)}")

    @staticmethod
    async def copy_collection_data(source_collection: str, target_collection: str) -> bool:
        try:
            db = Database.get_master_db()
            source = db[source_collection]
            target = db[target_collection]

            documents = await source.find().to_list(length=None)
            if documents:
                await target.insert_many(documents)

            return True
        except Exception as e:
            raise Exception(f"Failed to copy collection data: {str(e)}")