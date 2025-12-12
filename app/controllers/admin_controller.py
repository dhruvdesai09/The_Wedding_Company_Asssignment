from fastapi import APIRouter, HTTPException
from app.schemas.admin import AdminLogin, AdminLoginResponse
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(login_data: AdminLogin):
    service = AdminService()
    result = await service.authenticate(login_data)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return result