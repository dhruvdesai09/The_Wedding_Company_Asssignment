from pydantic import BaseModel, EmailStr
from datetime import datetime

class Admin(BaseModel):
    email: EmailStr
    hashed_password: str
    organization_name: str
    created_at: datetime