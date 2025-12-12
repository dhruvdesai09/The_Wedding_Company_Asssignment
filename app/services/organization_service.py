from typing import Optional, Dict
from datetime import datetime
from fastapi import HTTPException
from app.repositories.organization_repository import OrganizationRepository
from app.services.admin_service import AdminService
from app.services.collection_service import CollectionService
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse


class OrganizationService:
    def __init__(self):
        self.organization_repository = OrganizationRepository()
        self.admin_service = AdminService()
        self.collection_service = CollectionService()

    async def create_organization(self, org_data: OrganizationCreate) -> OrganizationResponse:
        if await self.organization_repository.exists(org_data.organization_name):
            raise HTTPException(status_code=400, detail="Organization already exists")

        collection_name = f"org_{org_data.organization_name}"

        admin_id = await self.admin_service.create_admin(
            email=org_data.email,
            password=org_data.password,
            organization_name=org_data.organization_name
        )

        organization_data = {
            "organization_name": org_data.organization_name,
            "collection_name": collection_name,
            "admin_id": admin_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.organization_repository.create(organization_data)

        await self.collection_service.create_organization_collection(collection_name)

        return OrganizationResponse(
            organization_name=org_data.organization_name,
            collection_name=collection_name,
            admin_email=org_data.email,
            created_at=organization_data["created_at"].isoformat()
        )

    async def get_organization(self, organization_name: str) -> Dict:
        organization = await self.organization_repository.find_by_name(organization_name)

        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        admin = await self.admin_service.get_admin_by_organization(organization_name)

        return {
            "organization_name": organization["organization_name"],
            "collection_name": organization["collection_name"],
            "admin_email": admin["email"] if admin else None,
            "created_at": organization["created_at"].isoformat(),
            "updated_at": organization["updated_at"].isoformat()
        }

    async def update_organization(self, org_data: OrganizationUpdate, old_org_name: str) -> OrganizationResponse:
        if org_data.organization_name != old_org_name:
            if await self.organization_repository.exists(org_data.organization_name):
                raise HTTPException(status_code=400, detail="New organization name already exists")

        old_organization = await self.organization_repository.find_by_name(old_org_name)
        if not old_organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        new_collection_name = f"org_{org_data.organization_name}"
        old_collection_name = old_organization["collection_name"]

        await self.collection_service.create_organization_collection(new_collection_name)

        await self.collection_service.copy_collection_data(old_collection_name, new_collection_name)

        admin = await self.admin_service.get_admin_by_organization(old_org_name)
        if admin:
            await self.admin_service.update_admin(admin["email"], org_data.password)
            await self.admin_service.admin_repository.update(
                admin["email"],
                {"organization_name": org_data.organization_name}
            )

        update_data = {
            "organization_name": org_data.organization_name,
            "collection_name": new_collection_name,
            "updated_at": datetime.utcnow()
        }

        await self.organization_repository.update(old_org_name, update_data)

        await self.collection_service.drop_organization_collection(old_collection_name)

        return OrganizationResponse(
            organization_name=org_data.organization_name,
            collection_name=new_collection_name,
            admin_email=org_data.email,
            created_at=old_organization["created_at"].isoformat()
        )

    async def delete_organization(self, organization_name: str, requester_org: str) -> Dict:
        if organization_name != requester_org:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this organization")

        organization = await self.organization_repository.find_by_name(organization_name)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        await self.collection_service.drop_organization_collection(organization["collection_name"])

        await self.admin_service.delete_admin_by_organization(organization_name)

        await self.organization_repository.delete(organization_name)

        return {"message": "Organization deleted successfully"}