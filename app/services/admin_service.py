from typing import Optional, Dict
from datetime import datetime
from app.repositories.admin_repository import AdminRepository
from app.utils.security import SecurityUtil
from app.schemas.admin import AdminLogin, AdminLoginResponse


class AdminService:
    def __init__(self):
        self.admin_repository = AdminRepository()
        self.security_util = SecurityUtil()

    async def create_admin(self, email: str, password: str, organization_name: str) -> str:
        hashed_password = self.security_util.hash_password(password)
        admin_data = {
            "email": email,
            "hashed_password": hashed_password,
            "organization_name": organization_name,
            "created_at": datetime.utcnow()
        }
        return await self.admin_repository.create(admin_data)

    async def authenticate(self, login_data: AdminLogin) -> Optional[AdminLoginResponse]:
        admin = await self.admin_repository.find_by_email(login_data.email)

        if not admin:
            return None

        if not self.security_util.verify_password(login_data.password, admin["hashed_password"]):
            return None

        token_data = {
            "admin_id": str(admin["_id"]),
            "organization_name": admin["organization_name"],
            "email": admin["email"]
        }
        access_token = self.security_util.create_access_token(token_data)

        return AdminLoginResponse(
            access_token=access_token,
            token_type="bearer",
            admin_id=str(admin["_id"]),
            organization_name=admin["organization_name"]
        )

    async def get_admin_by_organization(self, organization_name: str) -> Optional[Dict]:
        return await self.admin_repository.find_by_organization(organization_name)

    async def update_admin(self, email: str, new_password: str) -> bool:
        hashed_password = self.security_util.hash_password(new_password)
        return await self.admin_repository.update(email, {"hashed_password": hashed_password})

    async def delete_admin_by_organization(self, organization_name: str) -> bool:
        return await self.admin_repository.delete_by_organization(organization_name)