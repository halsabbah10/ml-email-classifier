from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from database import CategoryEnum

class EmailCreate(BaseModel):
    from_address: str
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    from_address: str
    subject: str
    body: str
    category: CategoryEnum
    received_at: datetime
    
    class Config:
        from_attributes = True