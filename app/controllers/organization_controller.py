from fastapi import APIRouter, Depends, HTTPException
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationGet,
    OrganizationDelete
)
from app.services.organization_service import OrganizationService
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/org", tags=["Organizations"])

@router.post("/create", response_model=OrganizationResponse)
async def create_organization(org_data: OrganizationCreate):
    service = OrganizationService()
    return await service.create_organization(org_data)

@router.get("/get")
async def get_organization(organization_name: str):
    service = OrganizationService()
    return await service.get_organization(organization_name)

@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    org_data: OrganizationUpdate,
    organization_name: str,
    token_data: dict = Depends(AuthMiddleware.verify_token)
):
    service = OrganizationService()
    return await service.update_organization(org_data, organization_name)

@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    token_data: dict = Depends(AuthMiddleware.verify_token)
):
    service = OrganizationService()
    requester_org = token_data.get("organization_name")
    return await service.delete_organization(organization_name, requester_org)