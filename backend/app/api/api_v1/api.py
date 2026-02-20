from fastapi import APIRouter
from app.api.api_v1.endpoints import login, users, tasks
from app.api.api_v1.endpoints import login, users, tasks, upload  # Add upload
from app.api.api_v1.endpoints import attachments

apirouter = APIRouter()

apirouter.include_router(login.router, tags=["login"])
apirouter.include_router(users.router, prefix="/users", tags=["users"])
apirouter.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
apirouter.include_router(upload.router, prefix="/upload", tags=["upload"])
apirouter.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
