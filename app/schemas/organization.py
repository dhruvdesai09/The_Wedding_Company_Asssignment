from pydantic import BaseModel, EmailStr, Field

class OrganizationCreate(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class OrganizationUpdate(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class OrganizationResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: str

class OrganizationGet(BaseModel):
    organization_name: str

class OrganizationDelete(BaseModel):
    organization_name: str