from typing import Optional, Dict
from datetime import datetime
from app.utils.database import Database
from bson import ObjectId


class OrganizationRepository:
    def __init__(self):
        self.db = Database.get_master_db()
        self.collection = self.db["organizations"]

    async def create(self, organization_data: Dict) -> str:
        result = await self.collection.insert_one(organization_data)
        return str(result.inserted_id)

    async def find_by_name(self, organization_name: str) -> Optional[Dict]:
        return await self.collection.find_one({"organization_name": organization_name})

    async def update(self, organization_name: str, update_data: Dict) -> bool:
        update_data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"organization_name": organization_name},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete(self, organization_name: str) -> bool:
        result = await self.collection.delete_one({"organization_name": organization_name})
        return result.deleted_count > 0

    async def exists(self, organization_name: str) -> bool:
        count = await self.collection.count_documents({"organization_name": organization_name})
        return count > 0