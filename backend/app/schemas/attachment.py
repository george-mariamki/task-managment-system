from datetime import datetime
from pydantic import BaseModel

# Schema für Anhänge (Attachments)
class AttachmentOut(BaseModel):
    id: int
    filename: str
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True
