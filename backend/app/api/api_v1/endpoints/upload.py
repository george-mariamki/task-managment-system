import os
import shutil
from typing import Any
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.attachment import Attachment  

router = APIRouter()

# Verzeichnis für hochgeladene Dateien
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# (Validation)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".txt"}

@router.post("/", response_model=dict)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Datei hochladen und Attachment-Eintrag in der DB erstellen.
    """
    # 1. Validierung (Dateityp)
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 2. Speichern auf der Festplatte
    # Wir fügen einen Timestamp hinzu, um Namenskonflikte zu vermeiden
    import time
    timestamp = int(time.time())
    safe_filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_location = f"{UPLOAD_DIR}/{safe_filename}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 3. Eintrag in der Datenbank erstellen (noch ohne Task-Zuweisung)
    db_attachment = Attachment(
        filename=file.filename,
        file_path=f"/{file_location}",
        file_type=file.content_type
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)

    # 4. ID und URL zurückgeben
    return {"id": db_attachment.id, "url": db_attachment.file_path, "filename": db_attachment.filename}
