from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Router einbinden
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
