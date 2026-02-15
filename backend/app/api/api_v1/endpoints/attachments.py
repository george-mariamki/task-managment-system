import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.delete("/{id}", response_model=schemas.AttachmentOut)
def delete_attachment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an attachment file from DB and disk.
    """
    attachment = crud.attachment.get(db=db, id=id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Check permissions: Ensure the user owns the task this attachment belongs to
    # OR if the attachment is not linked to any task yet (orphan), allow deletion by uploader (if we tracked uploader_id)
    # For now, we assume if it's linked, check task owner.
    if attachment.task_id:
        task = crud.task.get(db=db, id=attachment.task_id)
        if task and task.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")
            
    # Remove file from disk
    file_path_on_disk = attachment.file_path.lstrip("/")
    if os.path.exists(file_path_on_disk):
        os.remove(file_path_on_disk)

    # Remove from DB
    attachment = crud.attachment.remove(db=db, id=id)
    return attachment
