from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .attachment import AttachmentOut

# Gemeinsame Eigenschaften für alle Task-Schemas
class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = False

# Eigenschaften beim Erstellen (Title ist erforderlich)
class TaskCreate(TaskBase):
    title: str
    # Wir erwarten eine Liste von Attachment-IDs, die bereits hochgeladen wurden
    attachment_ids: list[int] = [] 

# Eigenschaften beim Aktualisieren
class TaskUpdate(TaskBase):
    new_attachment_ids: list[int] = [] 

# Eigenschaften bei der Anzeige aus der Datenbank
class TaskInDBBase(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    # Die Antwort enthält die vollen Attachment-Objekte
    attachments: list[AttachmentOut] = []

















