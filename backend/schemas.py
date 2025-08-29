from pydantic import BaseModel
from datetime import datetime
from typing import List
from database import CategoryEnum

class EmailCreate(BaseModel):
    from_address: str
    subject: str
    body: str

class EmailBatchUpload(BaseModel):
    emails: List[EmailCreate]

class BatchUploadResponse(BaseModel):
    success_count: int
    failed_count: int
    total_count: int
    failed_emails: List[dict]
    message: str

class EmailResponse(BaseModel):
    id: int
    from_address: str
    subject: str
    body: str
    category: CategoryEnum
    received_at: datetime
    
    class Config:
        from_attributes = True