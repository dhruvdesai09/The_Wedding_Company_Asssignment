from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Organization(BaseModel):
    organization_name: str
    collection_name: str
    admin_id: str
    created_at: datetime
    updated_at: datetime