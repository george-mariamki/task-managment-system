from fastapi import APIRouter
from app.api.api_v1.endpoints import login, users, tasks
from app.api.api_v1.endpoints import login, users, tasks, upload  # Add upload
from app.api.api_v1.endpoints import attachments

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
