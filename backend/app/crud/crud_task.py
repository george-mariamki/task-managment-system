from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.attachment import Attachment

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TaskCreate, owner_id: int
    ) -> Task:
        obj_in_data = jsonable_encoder(obj_in)
        
        # Attachment-IDs extrahieren und aus den Daten entfernen (da sie nicht im Task-Modell sind)
        attachment_ids = obj_in_data.pop("attachment_ids", [])
        if "attachment_url" in obj_in_data:
            del obj_in_data["attachment_url"]
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Jetzt die Anhänge verknüpfen
        if attachment_ids:
            # Wir suchen alle Attachments mit diesen IDs
            attachments = db.query(Attachment).filter(Attachment.id.in_(attachment_ids)).all()
            for attachment in attachments:
                attachment.task_id = db_obj.id  # Verknüpfung herstellen
                db.add(attachment)
            db.commit()
            db.refresh(db_obj)
            
        return db_obj
    
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Task,
        obj_in: TaskUpdate | dict
    ) -> Task:
        # 1. Daten vorbereiten (obj_in in dict umwandeln, falls es ein Pydantic-Modell ist)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # 2. Attachment-IDs extrahieren und aus den Daten entfernen (da sie nicht im Task-Modell sind)
        new_attachment_ids = update_data.pop("new_attachment_ids", [])

        # 3. Task-Objekt aktualisieren
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # 4. Neue Anhänge verknüpfen (falls neue_attachment_ids übergeben wurden)
        if new_attachment_ids:
            attachments = db.query(Attachment).filter(Attachment.id.in_(new_attachment_ids)).all()
            for attachment in attachments:
                attachment.task_id = db_obj.id
                db.add(attachment)
            db.commit()
            db.refresh(db_obj)

        return db_obj

task = CRUDTask(Task)
