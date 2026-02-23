import secrets
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.models.attachment import Attachment
from app.models.user import User
from app.utils.storage import build_public_url, ensure_upload_dir, sanitize_filename


router = APIRouter()


@router.post("/", response_model=dict)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Datei hochladen und Attachment-Eintrag in der DB erstellen.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Dateiname fehlt.")

    ensure_upload_dir()

    original_name = sanitize_filename(file.filename)
    ext = Path(original_name).suffix.lower()

    allowed = {e.lower() for e in settings.UPLOAD_ALLOWED_EXTENSIONS}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Ungültiger Dateityp.")

    ts = int(time.time())
    rnd = secrets.token_hex(8)
    stored_filename = f"{current_user.id}_{ts}_{rnd}_{original_name}"

    disk_path = (settings.upload_dir_abs / stored_filename).resolve()
    max_size = int(settings.UPLOAD_MAX_SIZE_MB * 1024 * 1024)

    total = 0
    try:
        with disk_path.open("wb") as out:
            while True:
                chunk = file.file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise HTTPException(status_code=413, detail="Datei ist zu groß.")
                out.write(chunk)
    except HTTPException:
        if disk_path.exists():
            disk_path.unlink(missing_ok=True)
        raise
    except Exception:
        if disk_path.exists():
            disk_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Upload fehlgeschlagen.")
    finally:
        try:
            file.file.close()
        except Exception:
            pass

    public_url = build_public_url(stored_filename)

    db_attachment = Attachment(
        filename=original_name,
        file_path=public_url,
        file_type=file.content_type,
    )

    try:
        db.add(db_attachment)
        db.commit()
        db.refresh(db_attachment)
    except Exception:
        if disk_path.exists():
            disk_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Datenbankfehler beim Speichern.")

    return {"id": db_attachment.id, "url": public_url, "filename": db_attachment.filename}
