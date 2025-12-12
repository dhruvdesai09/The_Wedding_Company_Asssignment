from typing import Optional, Dict
from app.utils.database import Database
from bson import ObjectId


class AdminRepository:
    def __init__(self):
        self.db = Database.get_master_db()
        self.collection = self.db["admins"]

    async def create(self, admin_data: Dict) -> str:
        result = await self.collection.insert_one(admin_data)
        return str(result.inserted_id)

    async def find_by_email(self, email: str) -> Optional[Dict]:
        return await self.collection.find_one({"email": email})

    async def find_by_organization(self, organization_name: str) -> Optional[Dict]:
        return await self.collection.find_one({"organization_name": organization_name})

    async def update(self, email: str, update_data: Dict) -> bool:
        result = await self.collection.update_one(
            {"email": email},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_by_organization(self, organization_name: str) -> bool:
        result = await self.collection.delete_one({"organization_name": organization_name})
        return result.deleted_count > 0