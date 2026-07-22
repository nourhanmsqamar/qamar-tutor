from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SessionResponse(BaseModel):
    id: int
    title: str
    document_name: str
    created_at: datetime
    last_message_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class RenameSessionRequest(BaseModel):
    title: str
