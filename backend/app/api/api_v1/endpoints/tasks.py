import os
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils.storage import disk_path_from_attachment_value


router = APIRouter()


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Lädt alle Tasks für den aktuellen Benutzer.
    """
    tasks = crud.task.get_multi_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=schemas.Task)
def create_task(
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Erstellt eine neue Aufgabe.
    """
    task = crud.task.create_with_owner(db=db, obj_in=task_in, owner_id=current_user.id)
    return task


@router.put("/{id}", response_model=schemas.Task)
def update_task(
    db: Session = Depends(deps.get_db),
    id: int = 0,
    task_in: schemas.TaskUpdate = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Aktualisiert eine Aufgabe.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task nicht gefunden.")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Nicht genug Berechtigungen.")

    task = crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.delete("/{id}", response_model=schemas.Task)
def delete_task(
    db: Session = Depends(deps.get_db),
    id: int = 0,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Löscht eine Aufgabe und entfernt alle zugehörigen Dateien von der Platte.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task nicht gefunden.")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Nicht genug Berechtigungen.")

    for attachment in task.attachments:
        disk_path = disk_path_from_attachment_value(attachment.file_path)
        if disk_path.exists() and disk_path.is_file():
            disk_path.unlink(missing_ok=True)

    task = crud.task.remove(db=db, id=id)
    return task
