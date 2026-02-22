from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils.storage import disk_path_from_attachment_value


router = APIRouter()


@router.get("/my-files/", tags=["attachments"])
def list_user_files(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """List current user's attachments"""
    attachments = crud.attachment.get_multi(db=db)  # أو filter by user/tasks
    return [
        {"id": a.id, "filename": a.filename, "url": f"{a.file_path}"}
        for a in attachments if a.task and a.task.owner_id == current_user.id
    ]

@router.delete("/{id}", response_model=schemas.AttachmentOut)
def delete_attachment(
    db: Session = Depends(deps.get_db),
    id: int = 0,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Löscht ein Attachment aus DB und entfernt die Datei von der Platte.
    """
    attachment = crud.attachment.get(db=db, id=id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment nicht gefunden.")

    if attachment.task_id:
        task = crud.task.get(db=db, id=attachment.task_id)
        if task and task.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Nicht genug Berechtigungen.")

    disk_path = disk_path_from_attachment_value(attachment.file_path)
    if disk_path.exists() and disk_path.is_file():
        disk_path.unlink(missing_ok=True)

    attachment = crud.attachment.remove(db=db, id=id)
    return attachment
